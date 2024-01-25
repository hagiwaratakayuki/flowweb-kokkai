from data_logics.kokkai_save import KokkaiLogic, KokkaiNodeModel


def process(loader, LogicClass=KokkaiLogic, ModelClass=KokkaiNodeModel):
    vectaizer
    model = buildModel()

    datas = loader('')
    logic = KokkaiLogic()

    vectors = vectaizer.exec(datas)

    return logic.save(vectors, model=model)
