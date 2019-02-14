from apicheck.model import BaseAPICheck


def model_to_dict(model: BaseAPICheck) -> dict:
    return model.__dict__
