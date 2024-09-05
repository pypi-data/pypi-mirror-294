SDXL_RESOLUTIONS = [
    (1024, 1024),
    (768, 1344),
    (832, 1216)
]

resolutions = {str(v[0]) + '×' + str(v[1]): v for v in SDXL_RESOLUTIONS}

downscale = 0.9

get_size = lambda r: int((r * downscale) // 8 * 8)

for pair in SDXL_RESOLUTIONS:
    v = (get_size(pair[0]), get_size(pair[1]))
    name = str(v[0]) + '×' + str(v[1]) + "[0.9]"
    resolutions[name] = v


default_resolution = "1024×1024"