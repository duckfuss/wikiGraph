# What is this

a bot to scrape and badly graph wikipedia

this is an educational project only

# Features

- multi language support
- graph simulation using spring physics
- search arbritrary breadth and depth of pages
- random starting pages

# What does it need

- selenium or BeautifulSoup  (scrape wikipedia)
- pygame    (display network)
- pymunk    (spring physics)
- firefox if using selenium

# Controls

## In main.py

| Control     | Effect                                                    |
| ----------- | --------------------------------------------------------- |
| maxSeed     | changes no. starting links                                |
| pageDepth   | no. pages explored per seed                               |
| pageBreadth | no. links explored per visited page                       |
| noOrphans   | (T/F) ensures there are no nodes without outgoing links   |
| scraper     | use either "Selenium" or "BeautifulSoup"                  |
| Language    | English, French, Chinese, Japanese, Spanish, Latin, Scots |

NB: non-latin script languages don't display nice!

## In app window

| Control       | Effect                                                    |
| ------------- | --------------------------------------------------------- |
| Left Click    | Highlight selected node and show it's children            |
| Left Drag     | Move node                                                 |
| Right Drag    | Pan                                                       |
| x (Def. ON)   | toggle node-node repulsion                                |
| c (Def. 0)   | toggle highlighting modes (see below)                     |
| v (Def. OFF) | Cancel velocity of all bodies                             |
| b (Def. OFF) | toggle text rendering (will still show on selected nodes) |
| m (Def. OFF)  | Toggle collisions between nodes                           |
| n (Def. OFF) | Freeze spring simulations                                 |

NB: toggling text rendering, node-node repulsion and collisions OFF can help performance for large graphs

### Highlighting modes:

0. (Default) clicking a node highlight's it's descendants with heatmap based off distance from selected node
1. highlight all nodes with heatmap based off number of parents (links IN)
2. Highlight all nodes with heatmap based off number of descendants

# Images:

<img width="400" alt="Screenshot 2025-05-27 at 12 39 13 pm" src="https://github.com/user-attachments/assets/407d2626-c16c-416c-b25d-77a6b953ecf9" />
<img width="300" alt="Screenshot 2025-05-27 at 10 35 31 am" src="https://github.com/user-attachments/assets/16e9e190-8328-4848-be76-e8657c3de354" />
<img width="300" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/8bee62c5-9c21-4e50-8a1d-148a67083a9f" />

### Highlighting mode 0 (Default)

<img width="750" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/5a1ee2b0-8a06-4550-9215-1f1013de77a2" />

### Highlighting mode 1 shows IN links:

<img width="750" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/5d1c6591-083e-4f7f-9f0c-dce88151bd46" />

### Highlighting mode 2 shows node depth:

<img width="750" alt="Screenshot 2025-05-27 at 10 39 36 am" src="https://github.com/user-attachments/assets/f425bb96-7f73-488d-8872-c305d609bcfa" />

## Larger example (graph with 2600 pages):

<img width="2227" alt="Screenshot 2025-06-04 at 10 33 48 am" src="https://github.com/user-attachments/assets/d38d9cea-d49d-424b-b831-a12e5552f483" />
