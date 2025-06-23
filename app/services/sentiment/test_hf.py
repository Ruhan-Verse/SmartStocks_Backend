from app.services.sentiment import huggingface

print(huggingface.analyze_sentiment("Tesla stock might go up soon!"))
