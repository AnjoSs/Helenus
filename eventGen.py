import random

events = ["Wrote a Line of Code",
          "Drank Mate",
          "Got Caffeine Shock"]
log = []

for i in range(0, 100):
    log.append(random.choice(events))

print(log)
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
