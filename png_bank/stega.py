from PIL import Image


def embed_message(path, message, terminator="ENDMESSAGEPNG"):
    image = import_image(path)
    m_embed = message + terminator
    # print(m_embed)
    width, height = image.size
    w = height * width * 3 / 8
    if len(m_embed) > w:
        print("Image size not sufficient for message")
        image.close()
        exit(0)
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            new_pixel = [None, None, None]
            for i in range(3):
                p_rgb = pixel[i]
                c_char_ind = ((x + y) * 3 + i) // 8
                if c_char_ind >= len(m_embed):
                    break
                c_char_bit = ((x + y) * 3 + i) % 8
                char_byte = bin(ord(m_embed[c_char_ind]))[2:].zfill(8)
                char_bin = int(char_byte[c_char_bit])
                b_val = (p_rgb >> 7) & 1
                b_val = b_val ^ ((p_rgb >> 6) & 1)
                b_val = b_val ^ ((p_rgb >> 5) & 1)
                b_val = b_val ^ char_bin
                new_pixel[i] = (pixel[i] & ~1) | b_val
            if None in new_pixel:
                for i, rgb in enumerate(new_pixel):
                    if rgb is None:
                        new_pixel[i] = pixel[i]
                image.putpixel((x, y), tuple(new_pixel))
                break
            image.putpixel((x, y), tuple(new_pixel))
    image.save(path)
    image.close()


def extract_message(path, terminator="ENDMESSAGEPNG"):
    image = import_image(path)
    width, height = image.size
    message = ''
    cbyte = ''
    for x in range(width):
        for y in range(height):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                p_rgb = pixel[i]
                b_val = (p_rgb >> 7) & 1
                b_val = b_val ^ ((p_rgb >> 6) & 1)
                b_val = b_val ^ ((p_rgb >> 5) & 1)
                b_val = b_val ^ (p_rgb & 1)
                cbyte += str(b_val)
                if len(cbyte) == 8:
                    message += chr(int(cbyte, 2))
                    t_ind = message.find(terminator)
                    if t_ind != -1:
                        image.close()
                        return message[:t_ind]
                    cbyte = ''


def import_image(path) -> Image:
    try:
        image = Image.open(path)
        image = image.convert("RGB")
        image.verify()
    except (FileNotFoundError, IOError):
        print(f"Error: The image at '{path}' could not be opened or is corrupted.")
        exit(0)

    return image
