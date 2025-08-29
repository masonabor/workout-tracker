from time import sleep

times = [0.34, 0.45, 0.12, 0.23, 3]
text = ['has', 'he', 'lost', 'his', 'mind?']
word = 'Black'

for i in range(5):
    print(text[i], end=' ', flush=True)
    sleep(times[i])

print(f'End of {word} Sabbat')
