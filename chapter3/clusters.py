from distances import pearson
from PIL import Image, ImageDraw 


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


def hcluster(rows, distance=pearson):
    distances = {}
    current_cluster_id = -1

    # Clusters are initially just the rows
    clust = [
        bicluster(rows[i], id=i)
        for i in range(len(rows))
    ]

    while len(clust) > 1:
        lowest_pair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # loop throught 
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculation
                clust_pair = (clust[i].id, clust[j].id)
                if clust_pair not in distances:
                    distances[clust_pair] = distance(clust[i].vec, clust[j].vec)

                d = distances[clust_pair]

                if d < closest:
                    closest = d
                    lowest_pair = (i, j)

        # calculate the average of the two Clusters
        merge_vec = [
            (clust[lowest_pair[0]].vec[i] + clust[lowest_pair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))
        ]

        # create new bicluster
        new_cluster = bicluster(
            merge_vec, left=clust[lowest_pair[0]], right=clust[lowest_pair[1]], 
            distance=closest, id=current_cluster_id
        )

        # clusters that weren't in the original set are negative
        current_cluster_id -= 1
        del clust[lowest_pair[1]]
        del clust[lowest_pair[0]]

        # append new larger cluster
        clust.append(new_cluster)
    return clust[0]


def print_clust(clust, labels=None, n=0):
    # indent to make hierarchy layout
    for i in range(n): print " ",

    if clust.id < 0:
        print "-"
    else:
        if not labels:
            print clust.id
        else:
            print labels[clust.id]

    if clust.left:
        print_clust(clust.left, labels=labels, n=n+1)
    if clust.right:
        print_clust(clust.right, labels=labels, n=n+1)


def get_height(clust):
    """Return height for given cluster"""
    # Is this an endpoint? The the height is just 1
    if not clust.left and not clust.right:
        return 1
    # Otherwise the height is the same of the heights of each branch
    return get_height(clust.left) + get_height(clust.right)


def get_depth(clust):
    """Return depth for given cluster"""
    # The distance of an endpoint is 0.0
    if not clust.left and not clust.right:
        return 0.0
    # The distance of a branch is the greater of its two sides plust its own distance
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


def draw_dendrogram(clust, labels, jpeg='clusters.jpg'):
    # height, width and depth
    h = get_height(clust) * 20
    w = 1200
    d = get_depth(clust) 

    # width is fixed so scale distances accordingly
    scaling = float(w - 150) / d

    # create new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw first node
    draw_node(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


def draw_node(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = get_height(clust.left) * 20
        h2 = get_height(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling

        # Vertical Line from this cluster to it's children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))
        # Horizontal line to left item 
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))
        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))
        # Call the funtion to draw the left and right nodes
        draw_node(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        draw_node(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # if this is an endpoint draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def rotate_matrix(data):
    """From give matrix of data, transpose it"""
    new_matrix = []
    for i in range(len(data[0])):
        new_matrix.append([data[j][i] for j in range(len(data))])
    return new_matrix

