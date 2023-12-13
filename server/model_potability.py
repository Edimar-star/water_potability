import numpy as np
import graphene
import joblib

model_potability = joblib.load('/app/server/models/model_potability.joblib')

class Prediction(graphene.ObjectType):
  predicionPotability = graphene.String()

class Query(graphene.ObjectType):
    waterPotability = graphene.List(Prediction, 
                                ph=graphene.Float(),
                                Hardness=graphene.Float(),
                                Solids=graphene.Float(),
                                Chloramines=graphene.Float(),
                                Sulfate=graphene.Float(),
                                Conductivity=graphene.Float(),
                                OrganicCarbon=graphene.Float(),
                                Trihalomethanes=graphene.Float(),
                                Turbidity=graphene.Float())

    def resolve_waterPotability(self, info, ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, OrganicCarbon, Trihalomethanes, Turbidity):
        input_ = np.array([[ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,OrganicCarbon,Trihalomethanes,Turbidity]])
        return [Prediction(predicionPotability=model_potability.predict(input_)[0])]

def water_potability(values):
    schema = graphene.Schema(query=Query)
    data = ",".join(values)
    query = """
    {
        waterPotability(""" + data + """){
            predicionPotability
        }
    }
    """
    result_ = schema.execute(query)
    return result_