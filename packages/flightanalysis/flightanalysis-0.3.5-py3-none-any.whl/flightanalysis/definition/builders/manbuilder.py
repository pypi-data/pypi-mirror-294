from flightanalysis.definition import (
    ManDef,
    ManParm,
    ManParms,
    ElDef,
    ElDefs,
    DummyMPs,
    Opp,
)
from typing import Callable
from functools import partial
from .elbuilders import line, loopmaker, rollmaker, stallturn, spin
import numpy as np
from flightanalysis.scoring.criteria.f3a_criteria import F3A
from flightanalysis.scoring.downgrade import DownGrades
from flightanalysis.scoring.f3a_downgrades import DGGrps

from dataclasses import dataclass, field


class MBTags:
    CENTRE = 0


def centred(elb):
    setattr(elb, "centred", True)
    return elb


c45 = np.cos(np.radians(45))


def r(turns):
    return 2 * np.pi * np.array(turns)


dp = DummyMPs()


@dataclass
class ManBuilder:
    mps: ManParms
    mpmaps: dict[str, dict]
    entry_line_dgs: DownGrades

    def __getattr__(self, name):
        if name in self.mpmaps:
            return partial(self.el, name)
        raise AttributeError(f"ManBuilder has no attribute {name}")

    def el(self, kind, *args, force_name=None, **kwargs):
        """Setup kwargs to pull defaults from mpmaps
        returns a function that appends the created elements to a ManDef"""

        all_kwargs = self.mpmaps[kind]["kwargs"].copy()  # take the defaults

        for k, a in kwargs.items():
            all_kwargs[k] = a  # take the **kwargs if they were specified

        all_kwargs.update(dict(zip(self.mpmaps[kind]["args"], args)))  # take the *args

        def append_el(md: ManDef, **kwargs) -> ElDefs:
            full_kwargs = {}
            for k, a in kwargs.items():
                if isinstance(a, str) or isinstance(a, Opp):
                    try:
                        a = ManParm.parse(
                            str(a), md.mps
                        )  # serialise and parse again to make sure its coming from this mandef
                    except Exception:
                        pass
                full_kwargs[k] = a

            eds, mps = self.mpmaps[kind]["func"](
                force_name if force_name else md.eds.get_new_name(), **full_kwargs
            )
            neds = md.eds.add(eds)
            md.mps.add(mps)
            return neds

        return partial(append_el, **all_kwargs)

    def create(
        self,
        maninfo,
        elmakers: list[Callable[[ManDef], ElDef]],
        elinedgs=None,
        **kwargs,
    ) -> ManDef:
        mps = self.mps.copy()
        for k, v in kwargs.items():
            if isinstance(v, ManParm):
                mps.add(v)
            elif isinstance(k, str):
                if k in mps.data:
                    mps[k].defaul = v
                else:
                    mps.add(ManParm.parse(v, mps, k))
        md = ManDef(maninfo, mps, ElDefs())

        entry_line = self.line(force_name="entry_line", length=30)(md)

        entry_line.dgs = elinedgs if elinedgs else self.entry_line_dgs

        for i, em in enumerate(elmakers, 1):
            if isinstance(em, int):
                if em == MBTags.CENTRE:
                    md.info.centre_points.append(len(md.eds.data))
            else:
                c1 = len(md.eds.data)
                try:
                    new_eds = em(md)
                except Exception as ex:
                    raise Exception(
                        f"Error running elmaker {i} of {md.info.name}"
                    ) from ex

                c2 = len(md.eds.data)

                if hasattr(em, "centred"):
                    if c2 - c1 == 1:
                        md.info.centred_els.append((c1, 0.5))

                    else:
                        ceid, fac = ElDefs(new_eds).get_centre(mps)
                        if abs(int(fac) - fac) < 0.05:
                            md.info.centre_points.append(c1 + ceid + int(fac))
                        else:
                            md.info.centred_els.append((ceid + c1, fac))

        md.mps = md.mps.remove_unused()
        return md


f3amb = ManBuilder(
    ManParms(
        [
            ManParm("speed", F3A.inter.speed, 30.0, "m/s"),
            ManParm("loop_radius", F3A.inter.radius, 55.0, "m"),
            ManParm("line_length", F3A.inter.length, 130.0, "m"),
            ManParm("point_length", F3A.inter.length, 20.0, "m"),
            ManParm("partial_roll_rate", F3A.inter.roll_rate, np.pi / 2, "rad/s"),
            ManParm("full_roll_rate", F3A.inter.roll_rate, 3 * np.pi / 4, "rad/s"),
            ManParm("snap_rate", F3A.inter.roll_rate, 4 * np.pi, "rad/s"),
            ManParm("stallturn_rate", F3A.inter.roll_rate, np.pi, "rad/s"),
            ManParm("spin_rate", F3A.inter.roll_rate, 1.7 * np.pi, "rad/s"),
            ManParm("ee_pause", F3A.inter.length, 20.0, "m"),
        ]
    ),
    mpmaps=dict(
        line=dict(
            func=line,
            args=[],
            kwargs=dict(
                speed="speed",
                length="line_length",
            ),
        ),
        loop=dict(
            func=loopmaker,
            args=["angle"],
            kwargs=dict(
                speed="speed",
                radius="loop_radius",
                rolls=0.0,
                ke=False,
                rollangle=None,
                rolltypes="roll",
                reversible=True,
                pause_length="point_length",
                break_angle=np.radians(10),
                snap_rate="snap_rate",
                break_roll=np.pi / 4,
                recovery_roll=np.pi / 2,
                mode="f3a",
            ),
        ),
        roll=dict(
            func=rollmaker,
            args=["rolls"],
            kwargs=dict(
                padded=True,
                reversible=True,
                speed="speed",
                line_length="line_length",
                partial_rate="partial_roll_rate",
                full_rate="full_roll_rate",
                pause_length="point_length",
                mode="f3a",
                break_angle=np.radians(10),
                snap_rate="snap_rate",
                break_roll=np.pi / 4,
                recovery_roll=np.pi / 2,
                rolltypes="roll",
            ),
        ),
        stallturn=dict(
            func=stallturn, args=[], kwargs=dict(speed=0.0, yaw_rate="stallturn_rate")
        ),
        snap=dict(
            func=rollmaker,
            args=["rolls"],
            kwargs=dict(
                padded=True,
                reversible=True,
                speed="speed",
                line_length="line_length",
                partial_rate="partial_roll_rate",
                full_rate="full_roll_rate",
                pause_length="point_length",
                mode="f3a",
                break_angle=np.radians(10),
                snap_rate="snap_rate",
                break_roll=np.pi / 4,
                recovery_roll=np.pi / 2,
                rolltypes="snap",
            ),
        ),
        spin=dict(
            func=spin,
            args=["turns"],
            kwargs=dict(
                speed=10,
                break_angle=np.radians(30),
                rate="spin_rate",
                nd_turns=np.pi / 4,
                recovery_turns=np.pi / 2,
            ),
        ),
    ),
    entry_line_dgs=DGGrps.exits,
)


imacmb = ManBuilder(
    ManParms(
        [
            ManParm("speed", F3A.inter.speed, 30.0, "m/s"),
            ManParm("loop_radius", F3A.inter.radius, 55.0, "m"),
            ManParm("line_length", F3A.inter.length, 130.0, "m"),
            ManParm("point_length", F3A.inter.length, 20.0, "m"),
            ManParm("partial_roll_rate", F3A.inter.roll_rate, np.pi, "rad/s"),
            ManParm("full_roll_rate", F3A.inter.roll_rate, np.pi, "rad/s"),
            ManParm("snap_rate", F3A.inter.roll_rate, 4 * np.pi, "rad/s"),
            ManParm("stallturn_rate", F3A.inter.roll_rate, 2 * np.pi, "rad/s"),
            ManParm("spin_rate", F3A.inter.roll_rate, 1.7 * np.pi, "rad/s"),
            ManParm("ee_pause", F3A.inter.length, 20.0, "m"),
        ]
    ),
    mpmaps=dict(
        line=dict(func=line, args=[], kwargs=dict(roll=0.0, speed=30.0, length=130)),
        loop=dict(
            func=loopmaker,
            args=["angle"],
            kwargs=dict(
                speed=30.0,
                radius=50,  #'loop_radius',
                rolls=0.0,
                ke=False,
                rollangle=None,
                rolltypes="roll",
                reversible=True,
                pause_length="point_length",
                break_angle=np.radians(15),
                snap_rate="snap_rate",
                break_rate=2 * np.pi,
                mode="imac",
            ),
        ),
        roll=dict(
            func=rollmaker,
            args=["rolls"],
            kwargs=dict(
                padded=True,
                reversible=True,
                speed=30.0,
                line_length=130,
                partial_rate="partial_roll_rate",
                full_rate="full_roll_rate",
                pause_length="point_length",
                mode="imac",
                break_angle=np.radians(15),
                snap_rate="snap_rate",
                break_rate=2 * np.pi,
                rolltypes="roll",
            ),
        ),
        stallturn=dict(
            func=stallturn, args=[], kwargs=dict(speed=0.0, yaw_rate="stallturn_rate")
        ),
        snap=dict(
            func=rollmaker,
            args=["rolls"],
            kwargs=dict(
                padded=True,
                reversible=True,
                speed=30.0,
                line_length="line_length",
                partial_rate="partial_roll_rate",
                full_rate="full_roll_rate",
                pause_length="point_length",
                mode="imac",
                break_angle=np.radians(15),
                snap_rate="snap_rate",
                break_rate=2 * np.pi,
                rolltypes="snap",
            ),
        ),
        spin=dict(
            func=spin,
            args=["turns"],
            kwargs=dict(
                speed=10,
                break_angle=np.radians(30),
                rate="spin_rate",
                break_rate=6,
                reversible=True,
            ),
        ),
    ),
    entry_line_dgs=DGGrps.line,
)
