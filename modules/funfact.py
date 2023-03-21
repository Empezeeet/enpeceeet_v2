import requests
class FunFactGenerator:
    def __init__(self):
        pass
    
    def getFunFact(self):
        req = requests.get("https://api.api-ninjas.com/v1/facts?limit=1", headers={'X-Api-Key': "BviBcIHYHYGqeOwHGcKY0w==LrFChK7JK0MV7N9K"})
        if req.status_code == requests.codes.ok:
            return str(req.json()[0]['fact'])
        else:
            print("Error:", req.status_code, req.text)
        
    
    
if __name__ == "__main__":
    print("SELF TEST")
    gen = FunFactGenerator()
    
    print(gen.getFunFact())
        