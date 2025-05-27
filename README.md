# What is this

a bot to scrape and badly graph wikipedia

this is an educational project only

# What does it need

- selenium  (scrape wikipedia)
- pygame    (display network)
- pymunk    (spring physics)

# Controls

| Control     | Effect                                                  |
| ----------- | ------------------------------------------------------- |
| maxSeed     | changes no. starting links                              |
| pageDepth   | no. pages explored per seed                             |
| pageBreadth | no. links explored per visited page                     |
| killOrphans | (T/F) ensures there are no nodes without outgoing links |
| Left click  | highlight selected node and it's children               |
| Left Drag   | move node                                               |
| Right Drag  | pan                                                     |
| m           | toggle collisions between nodes                         |
| n           | pause spring simulation                                 |
| ENTER       | cancel momentum of all bodies                           |

## Clickling a link highlights child links
<img width="400" alt="Screenshot 2025-05-27 at 12 39 13 pm" src="https://github.com/user-attachments/assets/407d2626-c16c-416c-b25d-77a6b953ecf9" />
<img width="300" alt="Screenshot 2025-05-27 at 10 34 32 am" src="https://github.com/user-attachments/assets/5ddc0b4a-b075-4bc4-9992-452f5711fe14" />
<img width="300" alt="Screenshot 2025-05-27 at 10 35 31 am" src="https://github.com/user-attachments/assets/16e9e190-8328-4848-be76-e8657c3de354" />
<img width="300" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/8bee62c5-9c21-4e50-8a1d-148a67083a9f" />
<img width="733" alt="Screenshot 2025-05-27 at 5 54 07 pm" src="https://github.com/user-attachments/assets/9229219d-2257-482e-b2ab-18c85f6075a8" />

## Larger example:

<img width="1000" alt="Screenshot 2025-05-25 at 5 06 41 pm" src="https://github.com/user-attachments/assets/73293462-0e31-4926-85a0-0fa72e173a1e" />
<img width="1000" alt="Screenshot 2025-05-25 at 5 06 56 pm" src="https://github.com/user-attachments/assets/344e64a9-fcb6-426c-979c-5f17a90c8353" />
