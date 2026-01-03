import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
import random


def random_transform(translate_x=(-1.0, 1.0),
                     translate_y=(-1.0, 1.0),
                     translate_z=(-1.0, 1.0),
                     rotate_x=(-10.0, 10.0),
                     rotate_y=(-10.0, 10.0),
                     rotate_z=(-10.0, 10.0),
                     scale_x=(0.8, 1.2),
                     scale_y=(0.8, 1.2),
                     scale_z=(0.8, 1.2)):
    for transform in pm.selected(type="transform"):
        transform.tx.set(transform.tx.get()+random.uniform(*translate_x))
        transform.ty.set(transform.ty.get()+random.uniform(*translate_y))
        transform.tz.set(transform.tz.get()+random.uniform(*translate_z))
        transform.rx.set(transform.rx.get()+random.uniform(*rotate_x))
        transform.ry.set(transform.ry.get()+random.uniform(*rotate_y))
        transform.rz.set(transform.rz.get()+random.uniform(*rotate_z))
        transform.sx.set(transform.sx.get()*random.uniform(*scale_x))
        transform.sy.set(transform.sy.get()*random.uniform(*scale_y))
        transform.sz.set(transform.sz.get()*random.uniform(*scale_z))