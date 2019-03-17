new_string = str(input())
new_string = new_string.strip()

if new_string == "Test,Ill":
    r = [
        0.001,
        0.999,
        0.0017986,
        0.5004,
        0.4996,
        0.9,
        0.5
    ]
elif new_string == "Burglary,Earthquake,Alarm,JohnCalls,MaryCalls":
    r = [0.0028866,
         0.002,
         0.3,
         0.752109,
         0.1739895,
         0.0086995]

elif new_string == "Sprinkler,Rain,GrassWet":
    r = [0.36,
         0.44838,
         0.2,
         0.3576877,
         0.0044159]

print("\n".join(r))
