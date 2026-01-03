

ACTIVE = enum("higGpu", "midGpu", "lowGpu", "higAss", "midAss", "lowAss", "higAbc", "midAbc", "lowAbc")


def assembly(active=ACTIVE):
    for assembly in pm.ls(type="assemblyReference", sl=1):
        pm.assembly(assembly, e=1, a=str(ACTIVE[active]))


