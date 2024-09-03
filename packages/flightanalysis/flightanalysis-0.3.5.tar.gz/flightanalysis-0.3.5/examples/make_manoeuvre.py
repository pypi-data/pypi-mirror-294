from flightplotting import plotsec, plot_regions
from flightplotting.traces import axis_rate_trace
from flightanalysis import (
    ManDef, BoxLocation, Position, Height, Direction, 
    Orientation, ManInfo, r, MBTags, c45, centred, ManParm, Combination)
import numpy as np
from flightanalysis.definition import f3amb
from flightdata import NumpyEncoder
import plotly.graph_objects as go
from json import dumps
import geometry as g

mdef: ManDef = f3amb.create(ManInfo(
    "Spin", "iSpin", k=3, position=Position.CENTRE, 
    start=BoxLocation(Height.TOP, Direction.UPWIND, Orientation.INVERTED),
    end=BoxLocation(Height.BTM),
),[
    MBTags.CENTRE,
    f3amb.spin(r(2)),
    f3amb.roll(r(0.5), line_length=165),
    f3amb.loop(np.pi/2),
])

data = mdef.to_dict()
print(dumps(data, indent=2, cls=NumpyEncoder))
mdef = ManDef.from_dict(data)

it = g.Transformation(g.Point(-20,150,50), mdef.info.initial_transform(150, 1).rotation)

man = mdef.create()

tp = man.create_template(it)

fig = plot_regions(tp, 'element', span=5)
fig = plotsec(tp, fig=fig, nmodels=10, scale=5)
#fig.add_traces(boxtrace())
fig.show()

fig = go.Figure(data=axis_rate_trace(tp))
fig.show()