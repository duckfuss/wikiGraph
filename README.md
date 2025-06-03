# What is this

a bot to scrape and badly graph wikipedia

this is an educational project only

# Features

- multi language support
- graph simulation using spring physics
- search arbritrary breadth and depth of pages
- random starting pages

# What does it need

- selenium  (scrape wikipedia)
- pygame    (display network)
- pymunk    (spring physics)
- firefox

# Controls

## In main.py

| Control     | Effect                                                    |
| ----------- | --------------------------------------------------------- |
| maxSeed     | changes no. starting links                                |
| pageDepth   | no. pages explored per seed                               |
| pageBreadth | no. links explored per visited page                       |
| noOrphans   | (T/F) ensures there are no nodes without outgoing links   |
| Language    | English, French, Chinese, Japanese, Spanish, Latin, Scots |

NB: non-latin script languages don't display nice!

## In app window

| Control       | Effect                                                    |
| ------------- | --------------------------------------------------------- |
| Left Click    | Highlight selected node and show it's children            |
| Left Drag     | Move node                                                 |
| Right Drag    | Pan                                                       |
| c (Def. 0)   | toggle highlighting modes (see below)                     |
| v (Def. OFF) | Cancel velocity of all bodies                             |
| b (Def. OFF) | toggle text rendering (will still show on selected nodes) |
| m (Def. OFF)  | Toggle collisions between nodes                           |
| n (Def. OFF) | Freeze spring simulations                                 |

NB: toggling text rendering and collisions OFF can help performance for large graphs 

### Highlighting modes:

0. (Default) clicking a node highlight's it's descendants with heatmap based off distance from selected node
1. highlight all nodes with heatmap based off number of parents (links IN)
2. Highlight all nodes with heatmap based off number of descendants

# Images:

<img width="400" alt="Screenshot 2025-05-27 at 12 39 13 pm" src="https://github.com/user-attachments/assets/407d2626-c16c-416c-b25d-77a6b953ecf9" />
<img width="300" alt="Screenshot 2025-05-27 at 10 34 32 am" src="https://github.com/user-attachments/assets/5ddc0b4a-b075-4bc4-9992-452f5711fe14" />
<img width="300" alt="Screenshot 2025-05-27 at 10 35 31 am" src="https://github.com/user-attachments/assets/16e9e190-8328-4848-be76-e8657c3de354" />
<img width="300" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/8bee62c5-9c21-4e50-8a1d-148a67083a9f" />

### Highlighting mode 1 shows hotspots:
<img width="300" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/44233d8a-ee1d-420f-8331-c6890946ac45" />



## Larger example:

<img width="1000" alt="Screenshot 2025-05-25 at 5 06 41 pm" src="https://github.com/user-attachments/assets/73293462-0e31-4926-85a0-0fa72e173a1e" />
<img width="1000" alt="Screenshot 2025-05-25 at 5 06 56 pm" src="https://github.com/user-attachments/assets/344e64a9-fcb6-426c-979c-5f17a90c8353" />
