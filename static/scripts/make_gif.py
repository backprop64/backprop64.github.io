from PIL import Image, ImageSequence

def create_alternating_gif(image_files, output_filename, duration):
    images = [Image.open(image).resize((256, 256)) for image in image_files]

    # Adjust duration to milliseconds
    duration_ms = int(duration * 1000)

    # Create gif frames
    frames = []
    for image in images:
        # If the image contains multiple frames, extract each frame
        if hasattr(image, 'n_frames') and image.n_frames > 1:
            for frame in ImageSequence.Iterator(image):
                frames.append(frame.copy())
        else:
            # Otherwise, use the single frame
            frames.append(image.copy())

    # Save gif
    frames[0].save(
        output_filename,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=duration_ms,
        loop=0
    )

image_files = ["static/img/redcaps_{}.jpeg".format(i) for i in range(3)]  # example image files
output_filename = "static/img/redcaps.gif"
duration = 1  # seconds per image

create_alternating_gif(image_files, output_filename, duration)
