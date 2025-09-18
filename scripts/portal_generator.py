import math
import random
import os
import json
from PIL import Image, ImageDraw


class SeamlessPlasmaPortalGenerator:
    def __init__(self, **kwargs):
        # Same as your original init
        self.size = kwargs.get("size", 16)
        self.frames = kwargs.get("frames", 16)
        self.num_spiral_layers = kwargs.get("num_spiral_layers", 3)
        self.rng = random.Random(kwargs.get("rng_seed", 100))

        # Visual props
        self.shimmer = kwargs.get("shimmer", 0.05)
        self.spiral_strength = kwargs.get("spiral_strength", 1.2)
        self.spiral_offset = kwargs.get("spiral_offset", -0.1)
        self.white_threshold = kwargs.get("white_threshold", 0.85)
        self.white_alpha = kwargs.get("white_alpha", 255)
        self.base_color = kwargs.get("base_color", (0, 180, 220))
        self.color_scale = kwargs.get("color_scale", (20, 75, 35))
        self.alpha_base = kwargs.get("alpha_base", 100)
        self.alpha_scale = kwargs.get("alpha_scale", 215)

        # Motion
        self.turbulence_strength = kwargs.get("turbulence_strength", 0.05)
        self.hotspot_prob = kwargs.get("hotspot_prob", 0.01)
        self.distortion_strength = kwargs.get("distortion_strength", 0.1)

        # Animation
        self.frametime = kwargs.get("frametime", 2)  # <-- NEW GLOBAL FRAMETIME

    # === plasma logic (unchanged) ===
    def color_map(self, n_color):
        r = int(self.base_color[0] + n_color * self.color_scale[0])
        g = int(self.base_color[1] + n_color * self.color_scale[1])
        b = int(self.base_color[2] + n_color * self.color_scale[2])
        return r, g, b

    def generate_spirals(self, x, y, time):
        n = 0.0
        for layer in range(self.num_spiral_layers):
            offset = (layer / self.num_spiral_layers) * 2 * math.pi
            u = (x + math.sin(time * 2 * math.pi + layer)) / self.size
            v = (y + math.cos(time * 2 * math.pi + layer)) / self.size
            u %= 1.0
            v %= 1.0
            spiral_x = (u - 0.5) * 2.0
            spiral_y = (v - 0.5) * 2.0
            mag = spiral_x**2 + spiral_y**2
            out_spiral = math.atan2(spiral_y, spiral_x)
            out_spiral += ((time * 2 * math.pi) - mag * 10 + layer * 2) * (1 if layer % 2 == 0 else -1)
            out_spiral = math.sin(out_spiral + offset) * 0.5 + 0.5
            out_spiral /= mag + 1
            n += out_spiral / self.num_spiral_layers
        return n

    def generate_turbulence(self, x, y, time):
        nx = (x / self.size) * 2 * math.pi
        ny = (y / self.size) * 2 * math.pi
        return (
            math.sin(nx + time * 2 * math.pi) * self.turbulence_strength
            + math.sin(ny - time * 2 * math.pi) * self.turbulence_strength
        )

    def apply_distortion(self, x, y, time):
        dx = math.sin((y / self.size) * 2 * math.pi + time * 2 * math.pi) * self.distortion_strength * self.size
        dy = math.cos((x / self.size) * 2 * math.pi - time * 2 * math.pi) * self.distortion_strength * self.size
        return (x + dx) % self.size, (y + dy) % self.size

    def setup_portal_sprite(self, time):
        output = Image.new("RGBA", (self.size, self.size))
        pixels = output.load()
        sin_time = time * 2 * math.pi

        for x in range(self.size):
            for y in range(self.size):
                xd, yd = self.apply_distortion(x, y, time)
                spiral_val = self.generate_spirals(xd, yd, time)
                turbulence_val = self.generate_turbulence(xd, yd, time)
                shimmer_val = self.rng.uniform(0.0, self.shimmer) + math.sin(
                    sin_time + ((x + y) / self.size) * math.pi
                ) * self.shimmer
                n = spiral_val + turbulence_val + shimmer_val
                n_adjusted = max(0.0, min(1.0, n * self.spiral_strength + self.spiral_offset))
                n_color = min(1.0, n_adjusted * 1.3)
                r, g, b = self.color_map(n_color)
                a = int(self.alpha_base + n_adjusted * self.alpha_scale)
                if n_adjusted > self.white_threshold and (self.rng.random() * 0.5 + 0.5) > 0.7:
                    r = g = b = a = self.white_alpha
                pixels[x, y] = (r, g, b, a)
        return output

    # === mcmeta helper ===
    def save_mcmeta(self, path):
        frames = list(range(self.frames))
        mcmeta = {
            "animation": {
                "frametime": self.frametime,
                "interpolate": True,
                "frames": frames
            }
        }
        with open(path + ".mcmeta", "w", encoding="utf-8") as f:
            json.dump(mcmeta, f, indent=2)
        print(f"Saved {path}.mcmeta")

    # === vanilla sheet ===
    def generate_portal_sheet(self, block_dir):
        os.makedirs(block_dir, exist_ok=True)
        output_file = os.path.join(block_dir, "nether_portal.png")
        sheet = Image.new("RGBA", (self.size, self.size * self.frames))
        for i in range(self.frames):
            time = i / self.frames
            frame = self.setup_portal_sprite(time)
            sheet.paste(frame, (0, i * self.size))
        sheet.save(output_file)
        print(f"Saved vanilla portal sheet → {output_file}")
        self.save_mcmeta(output_file)

    # === CTM compact ===
    def generate_ctm_tiles(self, ctm_dir):
        os.makedirs(ctm_dir, exist_ok=True)

        def apply_borders(img, mode):
            """Apply brightened borders depending on CTM mode (0–4)."""
            img = img.copy()
            pixels = img.load()
            for x in range(self.size):
                for y in range(self.size):
                    edge_factor = 0

                    if mode == 0 or mode == 2:  # vertical edges
                        if x < self.size * 0.25:
                            edge_factor = max(edge_factor, 1 - x / (self.size * 0.25))
                        if x > self.size * 0.75:
                            edge_factor = max(edge_factor, (x - self.size * 0.75) / (self.size * 0.25))
                    if mode == 0 or mode == 3:  # horizontal edges
                        if y < self.size * 0.25:
                            edge_factor = max(edge_factor, 1 - y / (self.size * 0.25))
                        if y > self.size * 0.75:
                            edge_factor = max(edge_factor, (y - self.size * 0.75) / (self.size * 0.25))
                    if mode == 4:  # corners only
                        in_left = x < self.size * 0.25
                        in_right = x > self.size * 0.75
                        in_top = y < self.size * 0.25
                        in_bottom = y > self.size * 0.75
                        if (in_left and in_top) or (in_right and in_top) or (in_left and in_bottom) or (in_right and in_bottom):
                            edge_factor = 1 - max(
                                min(x, self.size - 1 - x),
                                min(y, self.size - 1 - y),
                            ) / (self.size * 0.25)

                    if edge_factor > 0:
                        r, g, b, a = pixels[x, y]
                        r = min(255, int(r * (1 + 1.5 * edge_factor)))
                        g = min(255, int(g * (1 + 1.5 * edge_factor)))
                        b = min(255, int(b * (1 + 1.5 * edge_factor)))
                        pixels[x, y] = (r, g, b, a)
            return img

        for mode in range(5):
            sheet = Image.new("RGBA", (self.size, self.size * self.frames))
            for i in range(self.frames):
                time = i / self.frames
                frame = self.setup_portal_sprite(time)
                if mode != 1:  # mode 1 = center, no border changes
                    frame = apply_borders(frame, mode)
                sheet.paste(frame, (0, i * self.size))
            out_file = os.path.join(ctm_dir, f"{mode}.png")
            sheet.save(out_file)
            print(f"Saved CTM {mode}.png → {out_file}")
            self.save_mcmeta(out_file)


# === Example usage ===
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BLOCK_DIR = os.path.join(BASE_DIR, "..", "assets", "minecraft", "textures", "block")
    #CTM_DIR = os.path.join(BASE_DIR, "..", "assets", "minecraft", "optifine", "ctm", "nether", "portal")

    portal = SeamlessPlasmaPortalGenerator(
        size=16,
        frames=32,
        shimmer=0.05,
        white_threshold=0.85,
        turbulence_strength=0.05,
        hotspot_prob=0.02,
        distortion_strength=0.1,
        num_spiral_layers=4,
        base_color=(75, 15, 130),
        frametime=2,  # <-- adjustable globally
    )
    portal.generate_portal_sheet(BLOCK_DIR)
    #portal.generate_ctm_tiles(CTM_DIR)
