from __future__ import annotations
from dataclasses import dataclass
from ..el_analysis import ElementAnalysis
from flightdata import State
from flightanalysis.definition import ManDef, ElDef
from flightanalysis.manoeuvre import Manoeuvre
from flightanalysis.scoring import (
    Results,
    ManoeuvreResults,
    Measurement,
    ElementsResults,
    Result,
)
from flightanalysis.scoring.criteria.f3a_criteria import F3A
from flightanalysis.definition.maninfo import Position
from flightanalysis.elements import Element
import geometry as g
import numpy as np
from .basic import Basic
from .alignment import Alignment
from loguru import logger


@dataclass
class Complete(Alignment):
    corrected: Manoeuvre
    corrected_template: State

    @staticmethod
    def from_dict(data: dict, fallback=True):
        pa = Alignment.from_dict(data, fallback)
        try:
            pa = Complete(
                **pa.__dict__,
                corrected=Manoeuvre.from_dict(data["corrected"]),
                corrected_template=State.from_dict(data["corrected_template"]),
            )
        except Exception as e:
            if fallback:
                logger.debug(f"Failed to parse Complete: {repr(e)}")
            else:
                raise e
        return pa

    def run(self, optimise_aligment=True) -> Scored:
        if optimise_aligment:
            self = self.optimise_alignment()
        self = self.update_templates()
        return Scored(
            **self.__dict__,
            scores=ManoeuvreResults(self.inter(), self.intra(), self.positioning()),
        )

    @property
    def elnames(self):
        return list(self.mdef.eds.data.keys())

    def __iter__(self):
        for edn in list(self.mdef.eds.data.keys()):
            yield self.get_ea(edn)

    def __getitem__(self, i):
        return self.get_ea(self.mdef.eds[i + 1].name)

    def __getattr__(self, name):
        if name in self.mdef.eds.data.keys():
            return self.get_ea(name)
        raise AttributeError(f"Attribute {name} not found in {self.__class__.__name__}")

    def get_edef(self, name):
        return self.mdef.eds[name]

    def get_ea(self, name):
        el: Element = getattr(self.manoeuvre.all_elements(), name)
        st = el.get_data(self.flown)
        tp = el.get_data(self.template).relocate(st.pos[0])

        return ElementAnalysis(
            self.get_edef(name), self.mdef.mps, el, st, tp, el.ref_frame(tp)
        )

    def update_templates(self):
        if not len(self.flown) == len(self.template) or not np.all(
            self.flown.element == self.template.element
        ):
            manoeuvre, template = self.manoeuvre.match_intention(
                self.template[0], self.flown
            )
            mdef = ManDef(
                self.mdef.info,
                self.mdef.mps.update_defaults(self.manoeuvre),
                self.mdef.eds,
            )
            correction = mdef.create().add_lines()

            return Complete(
                self.id,
                mdef,
                self.flown,
                self.direction,
                manoeuvre,
                template,
                correction,
                correction.create_template(template[0], self.flown),
            )
        else:
            return self

    def get_score(
        self, eln: str, itrans: g.Transformation, fl: State
    ) -> tuple[Results, g.Transformation]:
        ed: ElDef = self.get_edef(eln)
        el: Element = self.manoeuvre.all_elements()[eln].match_intention(itrans, fl)
        tp = el.create_template(State.from_transform(itrans), fl)
        return ed.dgs.apply(el.uid, fl, tp, False), tp[-1].att

    def optimise_split(
        self, itrans: g.Transformation, eln1: str, eln2: str, fl: State
    ) -> int:
        el1: Element = self.manoeuvre.all_elements()[eln1]
        el2: Element = self.manoeuvre.all_elements()[eln2]

        def score_split(steps: int) -> float:
            new_fl = fl.shift_label(steps, 2, manoeuvre=self.name, element=eln1)
            res1, new_iatt = self.get_score(eln1, itrans, el1.get_data(new_fl))

            el2fl = el2.get_data(new_fl)
            res2 = self.get_score(
                eln2, g.Transformation(new_iatt, el2fl[0].pos), el2fl
            )[0]
            logger.debug(f"split {steps} {res1.total + res2.total:.2f}")
            logger.debug(
                f"e1={eln1}, e2={eln2}, steps={steps}, dg={res1.total + res2.total:.2f}"
            )
            return res1.total + res2.total

        dgs = {0: score_split(0)}

        steps = int(len(el1.get_data(fl)) > len(el2.get_data(fl))) * 2 - 1

        new_dg = score_split(steps)
        if new_dg > dgs[0]:
            steps = -steps
        else:
            steps += np.sign(steps)
            dgs[steps] = new_dg

        while True:
            if (steps > 0 and len(el2.get_data(fl)) <= steps + 3) or (
                steps < 0 and len(el1.get_data(fl)) <= -steps + 3
            ):
                break
            new_dg = score_split(steps)

            if new_dg < list(dgs.values())[-1]:
                dgs[steps] = new_dg
                steps += np.sign(steps)
            else:
                break
        min_dg_step = np.argmin(np.array(list(dgs.values())))
        out_steps = list(dgs.keys())[min_dg_step]
        return out_steps

    def optimise_alignment(self):
        fl = self.flown.copy()
        elns = list(self.mdef.eds.data.keys())

        padjusted = set(elns)
        count = 0
        while len(padjusted) > 0 and count < 2:
            adjusted = set()
            for eln1, eln2 in zip(elns[:-1], elns[1:]):
                if (eln1 in padjusted) or (eln2 in padjusted):
                    itrans = g.Transformation(
                        self.manoeuvre.all_elements()[eln1]
                        .get_data(self.template)[0]
                        .att,
                        self.manoeuvre.all_elements()[eln1].get_data(fl)[0].pos,
                    )
                    steps = self.optimise_split(itrans, eln1, eln2, fl)

                    if not steps == 0:
                        logger.debug(
                            f"Adjusting split between {eln1} and {eln2} by {steps} steps"
                        )

                        fl = fl.shift_label(steps, 2, manoeuvre=self.name, element=eln1)

                        adjusted.update([eln1, eln2])

            padjusted = adjusted
            count += 1
            logger.debug(
                f"pass {count}, {len(padjusted)} elements adjusted:\n{padjusted}"
            )

        return Basic(self.id, self.mdef, fl, self.direction).proceed()

    def side_box(self):
        meas = Measurement.side_box(self.flown)
        errors, dgs, keys = F3A.intra.box(F3A.intra.box.prepare(meas.value))
        return Result(
            "side box",
            meas,
            meas.value,
            np.arange(len(meas.value)),
            errors,
            dgs * meas.visibility[keys],
            keys,
            F3A.intra.box,
        )

    def top_box(self):
        meas = Measurement.top_box(self.flown)
        errors, dgs, keys = F3A.intra.box(F3A.intra.box.prepare(meas.value))
        return Result(
            "top box",
            meas,
            meas.value,
            np.arange(len(meas.value)),
            errors,
            dgs * meas.visibility[keys],
            keys,
            F3A.intra.box,
        )
        # return F3A.intra.box("top box", Measurement.top_box(self.flown))

    def create_centre_result(self, name: str, st: State) -> Result:
        meas = Measurement.centre_box(st)
        errors, dgs, keys = F3A.intra.angle(meas.value)
        return Result(
            name,
            meas,
            meas.value,
            np.arange(len(meas.value)),
            errors,
            dgs * meas.visibility[keys],
            keys,
            F3A.intra.angle,
        )

    def centre(self):
        results = Results("centres")
        for cpid in self.mdef.info.centre_points:
            if cpid == len(self.manoeuvre.elements):
                st = self.manoeuvre.elements[-1].get_data(self.flown)[-1]
            else:
                st = self.manoeuvre.elements[cpid].get_data(self.flown)[0]
            results.add(self.create_centre_result(f"centre point {cpid}", st))

        for ceid, fac in self.mdef.info.centred_els:
            ce = self.manoeuvre.elements[ceid].get_data(self.flown)
            path_length = (abs(ce.vel) * ce.dt).cumsum()
            id = np.abs(path_length - path_length[-1] * fac).argmin()
            results.add(
                self.create_centre_result(
                    f"centred element {ceid}", State(ce.data.iloc[[id], :])
                )
            )

        if len(results) == 0 and self.mdef.info.position == Position.CENTRE:
            al = State(
                self.flown.data.loc[
                    (self.flown.data.element != "entry_line")
                    & (self.flown.data.element != "exit_line")
                ]
            )
            midy = (np.max(al.y) + np.min(al.y)) / 2
            midid = np.abs(al.pos.y - midy).argmin()
            results.add(self.create_centre_result("centred manoeuvre", al[midid]))

        return results

    def distance(self):
        # TODO doesnt quite cover it, stalled manoeuvres could drift to > 170 for no downgrade
        meas = Measurement.depth(self.flown)
        mistakes, dgs, dgids = F3A.intra.depth(F3A.intra.depth.prepare(meas.value))
        return Result(
            "distance",
            meas,
            meas.value,
            np.arange(len(meas.value)),
            mistakes,
            dgs * meas.visibility[dgids],  # should be weighted average visibility
            dgids,
            F3A.intra.depth,
        )

    def intra(self):
        return ElementsResults([ea.intra_score() for ea in self])

    def inter(self):
        return self.mdef.mps.collect(self.manoeuvre, self.template)

    def positioning(self):
        pres = Results("positioning")
        if self.mdef.info.position == Position.CENTRE:
            pres.add(self.centre())
        tp_width = max(self.corrected_template.y) - min(self.corrected_template.y)
        if tp_width < 10:
            pres.add(self.distance())
        tb = self.top_box()
        if tb.total > 0:
            pres.add(self.top_box())
        sb = self.side_box()
        if sb.total > 0:
            pres.add(self.side_box())
        return pres

    def plot_3d(self, **kwargs):
        from flightplotting import plotsec, plotdtw

        fig = plotdtw(self.flown, self.flown.data.element.unique())
        return plotsec(self.flown, color="blue", nmodels=20, fig=fig, **kwargs)


from .scored import Scored  # noqa: E402
