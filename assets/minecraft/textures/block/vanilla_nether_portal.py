import math
import random
from PIL import Image

class PortalGenerator:
    def __init__(
        self,
        size=16,
        frames=16,
        shimmer=0.05,
        spiral_strength=1.2,
        spiral_offset=-0.1,
        white_threshold=0.85,
        white_alpha=255,
        base_color=(0, 180, 220),    # base RGB
        color_scale=(20, 75, 35),    # how much each channel is boosted by n_color
        alpha_base=100,
        alpha_scale=215,
        turbulence_strength=0.05,
        rng_seed=100
    ):
        self.size = size
        self.frames = frames
        self.shimmer = shimmer
        self.spiral_strength = spiral_strength
        self.spiral_offset = spiral_offset
        self.white_threshold = white_threshold
        self.white_alpha = white_alpha
        self.base_color = base_color
        self.color_scale = color_scale
        self.alpha_base = alpha_base
        self.alpha_scale = alpha_scale
        self.turbulence_strength = turbulence_strength
        self.rng = random.Random(rng_seed)

    def color_map(self, n_color):
        r = int(self.base_color[0] + n_color * self.color_scale[0])
        g = int(self.base_color[1] + n_color * self.color_scale[1])
        b = int(self.base_color[2] + n_color * self.color_scale[2])
        return r, g, b
        
    def generate_spirals(self, x, y, time):
        n = 0.0
        for dir in range(2):
            spiral_x = (x - dir * (self.size // 2)) / self.size * 2.0
            spiral_y = (y - dir * (self.size // 2)) / self.size * 2.0

            if spiral_x < -1:
                spiral_x += 2
            elif spiral_x >= 1:
                spiral_x -= 2
            if spiral_y < -1:
                spiral_y += 2
            elif spiral_y >= 1:
                spiral_y -= 2

            mag = spiral_x ** 2 + spiral_y ** 2
            out_spiral = math.atan2(spiral_y, spiral_x)
            out_spiral += ((time * math.pi * 2) - (mag * 10) + (dir * 2)) * (dir * 2 - 1)
            out_spiral = math.sin(out_spiral) * 0.5 + 0.5
            out_spiral /= mag + 1
            n += out_spiral / 2
        return n

    def generate_turbulence(self, x, y, time):
        nx = (x + y * 0.5) / self.size * 4.0
        ny = (y - x * 0.5) / self.size * 4.0
        return (
            math.sin(nx + time * 2 * math.pi) * self.turbulence_strength +
            math.sin(ny - time * 2 * math.pi) * self.turbulence_strength
        )

    def setup_portal_sprite(self, time):
        output = Image.new("RGBA", (self.size, self.size))
        pixels = output.load()

        for x in range(self.size):
            for y in range(self.size):
                n = self.generate_spirals(x, y, time)
                n += self.generate_turbulence(x, y, time)

                # shimmer
                n += self.rng.uniform(0.0, self.shimmer)
                n += math.sin((time * 2 * math.pi) + (x + y) * 0.05) * self.shimmer

                n_adjusted = max(0.0, min(1.0, n * self.spiral_strength + self.spiral_offset))
                n_color = min(1.0, n_adjusted * 1.3)

                r, g, b = self.color_map(n_color)
                a = int(self.alpha_base + n_adjusted * self.alpha_scale)

                if n_adjusted > self.white_threshold:
                    r = g = b = a = self.white_alpha

                pixels[x, y] = (
                    max(0, min(255, r)),
                    max(0, min(255, g)),
                    max(0, min(255, b)),
                    max(0, min(255, a))
                )

        return output

    def generate_portal_sheet(self, output_file="nether_portal.png"):
        sheet = Image.new("RGBA", (self.size, self.size * self.frames))
        for i in range(self.frames):
            time = i / self.frames
            frame = self.setup_portal_sprite(time)
            sheet.paste(frame, (0, i * self.size))
        sheet.save(output_file)
        print(f"Saved {output_file} with {self.frames} frames")

# Example usage
if __name__ == "__main__":
    portal = PortalGenerator(
        size=16,
        frames=32,
        shimmer=0.05,
        white_threshold=0.85,
        turbulence_strength=0.05,
    )
    portal.generate_portal_sheet()
