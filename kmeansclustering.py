from PIL import Image
import random
import math

# define some global colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
SKIN = [203, 144, 103]
# returns a 2D matrix for height and width width array is of the form [x, y, cluster]
def k_means(image, c1, c2, c3, c4, c5, c6):

    height_matrix = []
    for i in range(image.height):
        width_arr = []
        for j in range(image.width):

            p = image.getpixel((j, i))

            # assign the pixel to a cluster based on color
            dist_c1 = math.sqrt((p[0] - c1[0])**2 + (p[1] - c1[1])**2 + (p[2] - c1[2])**2)
            dist_c2 = math.sqrt((p[0] - c2[0])**2 + (p[1] - c2[1])**2 + (p[2] - c2[2])**2)
            dist_c3 = math.sqrt((p[0] - c3[0])**2 + (p[1] - c3[1])**2 + (p[2] - c3[2])**2)
            dist_c4 = math.sqrt((p[0] - c4[0])**2 + (p[1] - c4[1])**2 + (p[2] - c4[2])**2)
            dist_c5 = math.sqrt((p[0] - c5[0])**2 + (p[1] - c5[1])**2 + (p[2] - c5[2])**2)
            dist_c6 = math.sqrt((p[0] - c6[0])**2 + (p[1] - c6[1])**2 + (p[2] - c6[2])**2)

            if min(dist_c1, dist_c2, dist_c3, dist_c4, dist_c5, dist_c6) == dist_c1:
                width_arr.append(1)
            elif min(dist_c1, dist_c2, dist_c3, dist_c4, dist_c5, dist_c6) == dist_c2:
                width_arr.append(2)
            elif min(dist_c1, dist_c2, dist_c3, dist_c4, dist_c5, dist_c6) == dist_c3:
                width_arr.append(3)
            elif min(dist_c1, dist_c2, dist_c3, dist_c4, dist_c5, dist_c6) == dist_c4:
                width_arr.append(4)
            elif min(dist_c1, dist_c2, dist_c3, dist_c4, dist_c5, dist_c6) == dist_c5:
                width_arr.append(5)
            else:
                width_arr.append(6)

        height_matrix.append(width_arr)
    # return the height matrix
    return height_matrix

# returns for each pixel, 3 probability maps,
# a probability map is an array for each pixel of the porm [P(c1), P(c2), P(c3)]
def get_probability_maps(image, mat):
    
    # find the probability P(xy = c)
    p_height = []
    for y in range(image.height):
        p_width = []
        for x in range(image.width):
            c1_count = 0
            c2_count = 0
            c3_count = 0
            c4_count = 0
            c5_count = 0
            c6_count = 0
            for i in range(len(mat)):
                if mat[i][y][x] == 1:
                    c1_count += 1
                elif mat[i][y][x] == 2:
                    c2_count += 1
                elif mat[i][y][x] == 3:
                    c3_count += 1
                elif mat[i][y][x] == 4:
                    c4_count += 1
                elif mat[i][y][x] == 5:
                    c5_count += 1
                else:
                    c6_count += 1
            # after getting counts append the probability map of that pixel to the width array
            # probability will be out of 99 since there are only 99 chances for a cluster to flip in 100 runs
            p_width.append([
                (c1_count / 100), 
                (c2_count / 100), 
                (c3_count / 100), 
                (c4_count / 100), 
                (c5_count / 100), 
                (c6_count / 100)
            ])
        p_height.append(p_width)
    
    return p_height



def color_clustering(img_src, out_src):
    # first image
    with Image.open(img_src) as image:
        numofexec = 0
        centroids = [[],[],[]]
        out_matrix = []
        c1 = None
        c2 = None
        c3 = None
        c4 = None
        c5 = None
        c6 = None
        
        # repeat k-means 51 times
        for x in range(101):
            #randomly choose 3 pixels
            random_pixels = []
            for i in range(6):
                rand_x = random.randint(0, image.width - 1)
                rand_y = random.randint(0, image.height - 1)
                rand_pixel = image.getpixel((rand_x, rand_y))
                random_pixels.append(rand_pixel)

            # c1 is pixels closest to skin
            # c2 is pixels closest to black
            # c3 is pixel closest to white
            # c4 is pixel closest to red
            # c5 is pixel closest to green
            # c6 is pixel closest to blue

            # for each pixel find the distance to the base color 
            black_dists = []
            white_dists = []
            red_dists = []
            green_dists = []
            blue_dists = []
            skin_dists = []
            for i in range(len(random_pixels)):
                skin_dists.append(math.dist(random_pixels[i], SKIN))
                black_dists.append(math.dist(random_pixels[i], BLACK))
                white_dists.append(math.dist(random_pixels[i], WHITE))
                red_dists.append(math.dist(random_pixels[i], RED))
                green_dists.append(math.dist(random_pixels[i], GREEN))
                blue_dists.append(math.dist(random_pixels[i], BLUE))
                    

            # select the closest pixel to skin
            c1 = random_pixels[skin_dists.index(min(skin_dists))]
            # remove the pixel from the lists
            random_pixels.pop(skin_dists.index(min(skin_dists)))
            blue_dists.pop(skin_dists.index(min(skin_dists)))
            green_dists.pop(skin_dists.index(min(skin_dists)))
            red_dists.pop(skin_dists.index(min(skin_dists)))
            white_dists.pop(skin_dists.index(min(skin_dists)))
            black_dists.pop(skin_dists.index(min(skin_dists)))
            skin_dists.pop(skin_dists.index(min(skin_dists)))

            # select the minimum black distance
            c2 = random_pixels[black_dists.index(min(black_dists))]
            random_pixels.pop(black_dists.index(min(black_dists)))
            blue_dists.pop(black_dists.index(min(black_dists)))
            green_dists.pop(black_dists.index(min(black_dists)))
            red_dists.pop(black_dists.index(min(black_dists)))
            white_dists.pop(black_dists.index(min(black_dists)))
            black_dists.pop(black_dists.index(min(black_dists)))

            # select the minimum white distance
            c3 = random_pixels[white_dists.index(min(white_dists))]
            random_pixels.pop(white_dists.index(min(white_dists)))
            blue_dists.pop(white_dists.index(min(white_dists)))
            green_dists.pop(white_dists.index(min(white_dists)))
            red_dists.pop(white_dists.index(min(white_dists)))
            white_dists.pop(white_dists.index(min(white_dists)))

            # select the minimum red distance
            c4 = random_pixels[red_dists.index(min(red_dists))]
            random_pixels.pop(red_dists.index(min(red_dists)))
            blue_dists.pop(red_dists.index(min(red_dists)))
            green_dists.pop(red_dists.index(min(red_dists)))
            red_dists.pop(red_dists.index(min(red_dists)))

            # select the minimum green distance
            c5 = random_pixels[green_dists.index(min(green_dists))]
            random_pixels.pop(green_dists.index(min(green_dists)))
            blue_dists.pop(green_dists.index(min(green_dists)))
            green_dists.pop(green_dists.index(min(green_dists)))

            # select the minimum blue distance
            c6 = random_pixels[blue_dists.index(min(blue_dists))]
            random_pixels.pop(blue_dists.index(min(blue_dists)))
            blue_dists.pop(blue_dists.index(min(blue_dists)))


            # get the oputput from k means for this iteration
            out_matrix.append(k_means(image, c1, c2, c3, c4, c5, c6))
            numofexec += 1
        # get 3 probability maps for each pixel
        # P(X = cluster), 10 repititions of k-means, each pixel
        p_maps = get_probability_maps(image, out_matrix)

        # create a new image
        clustered_img = Image.new("RGB", image.size)

        # export new image rows with thresholds
        print("Skin pixels probability maps:")
        for y in range(len(p_maps)):
            for x in range(len(p_maps[y])):
                if p_maps[y][x].index(max(p_maps[y][x])) == 0:
                    if p_maps[y][x][0] >= 0.65:
                        print("({}, {}): {}".format(x, y, p_maps[y][x]))
                        clustered_img.putpixel((x, y), (0, 255, 255))
                    else:
                        clustered_img.putpixel((x, y), (0, 0, 0))
                elif p_maps[y][x].index(max(p_maps[y][x])) == 1:
                    clustered_img.putpixel((x, y), (0, 0, 0))
                elif p_maps[y][x].index(max(p_maps[y][x])) == 2:
                    clustered_img.putpixel((x, y), (0, 0, 0))
                elif p_maps[y][x].index(max(p_maps[y][x])) == 3:
                    clustered_img.putpixel((x, y), (0, 0, 0))
                elif p_maps[y][x].index(max(p_maps[y][x])) == 4:
                    clustered_img.putpixel((x, y), (0, 0, 0))
                else:
                    clustered_img.putpixel((x, y), (0, 0, 0))
        clustered_img.save(out_src)
        


def main():
    print("Starting clustering for image 1.")
    color_clustering("Image1.JPG", "Image1_clustered.JPG")
    print("Image 1 done: output = Image1_clustered.JPG.")
    print("Starting clustering for image 2.")
    color_clustering("Image2.JPG", "Image2_clustered.JPG")
    print("Image 2 done: output = Image2_clustered.JPG.")


if __name__ == "__main__":
    main()