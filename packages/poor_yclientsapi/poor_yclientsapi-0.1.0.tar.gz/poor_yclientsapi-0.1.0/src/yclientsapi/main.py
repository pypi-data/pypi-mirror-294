class YclientsAPI:
    def __init__(self, company_id: int, api_key: str):
        self.company_id = company_id
        self.api_key = api_key

    def say_hi(self):
        print("Hi!")
