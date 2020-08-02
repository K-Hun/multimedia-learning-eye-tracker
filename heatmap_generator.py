import heatmap as htmap

example_points = [(100, 20), (120, 25), (200, 50), (60, 300), (170, 250)]
example_img_path = 'lenna.png'
example_img = htmap.Image.open(example_img_path)
heatmapper = htmap.Heatmapper()
heatmap = heatmapper.heatmap_on_img(example_points, example_img)
heatmap.save('lenna_heatmap.png')
