from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)

# النظام الخبير كما هو
class DigestiveExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = []

    @Rule(Fact(symptom='إسهال'), Fact(symptom='مغص'), Fact(symptom='قيء'))
    def gastro(self):
        self.result.append("🔎 التهاب المعدة والأمعاء")

    @Rule(Fact(symptom='حرقة'), Fact(symptom='ارتجاع'))
    def reflux(self):
        self.result.append("🔥 ارتجاع مريئي")

@app.route("/", methods=["GET", "POST"])
def index():
    diagnosis = ""
    if request.method == "POST":
        symptoms = request.form.getlist("symptoms")
        engine = DigestiveExpertSystem()
        engine.reset()
        for s in symptoms:
            engine.declare(Fact(symptom=s))
        engine.run()
        diagnosis = "<br>".join(engine.result) if engine.result else "❓ لا يوجد تشخيص واضح."
    return render_template("index.html", diagnosis=diagnosis)

if __name__ == "__main__":
    app.run(debug=True)