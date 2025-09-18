import math
import random
from PIL import Image


class SeamlessPlasmaPortalGenerator:
    def __init__(
        self,
        size=16,
        frames=16,
        shimmer=0.05,
        spiral_strength=1.2,
        spiral_offset=-0.1,
        white_threshold=0.85,
        white_alpha=255,
        base_color=(0, 180, 220),
        color_scale=(20, 75, 35),
        alpha_base=100,
        alpha_scale=215,
        turbulence_strength=0.05,
        hotspot_prob=0.01,
        distortion_strength=0.1,
        num_spiral_layers=3,
        rng_seed=100,
    ):
        # Core parameters
        self.size = size
        self.frames = frames
        self.num_spiral_layers = num_spiral_layers
        self.rng = random.Random(rng_seed)

        # Visual properties
        self.shimmer = shimmer
        self.spiral_strength = spiral_strength
        self.spiral_offset = spiral_offset
        self.white_threshold = white_threshold
        self.white_alpha = white_alpha
        self.base_color = base_color
        self.color_scale = color_scale
        self.alpha_base = alpha_base
        self.alpha_scale = alpha_scale

        # Distortion / motion
        self.turbulence_strength = turbulence_strength
        self.hotspot_prob = hotspot_prob
        self.distortion_strength = distortion_strength

    def color_map(self, n_color):
        """Map normalized color value to RGB."""
        r = int(self.base_color[0] + n_color * self.color_scale[0])
        g = int(self.base_color[1] + n_color * self.color_scale[1])
        b = int(self.base_color[2] + n_color * self.color_scale[2])
        return r, g, b

    def generate_spirals(self, x, y, time):
        """Generate spiral noise for a given coordinate and time."""
        n = 0.0
        for layer in range(self.num_spiral_layers):
            offset = (layer / self.num_spiral_layers) * 2 * math.pi

            # Normalize coordinates for seamless wrapping
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
        """Generate small turbulence to add shimmer to the portal."""
        nx = (x / self.size) * 2 * math.pi
        ny = (y / self.size) * 2 * math.pi
        return (
            math.sin(nx + time * 2 * math.pi) * self.turbulence_strength
            + math.sin(ny - time * 2 * math.pi) * self.turbulence_strength
        )

    def apply_distortion(self, x, y, time):
        """Apply toroidal distortion for smooth motion."""
        dx = math.sin((y / self.size) * 2 * math.pi + time * 2 * math.pi) * self.distortion_strength * self.size
        dy = math.cos((x / self.size) * 2 * math.pi - time * 2 * math.pi) * self.distortion_strength * self.size
        return (x + dx) % self.size, (y + dy) % self.size

    def setup_portal_sprite(self, time):
        """Generate a single frame of the portal (refactored for clarity)."""
        output = Image.new("RGBA", (self.size, self.size))
        pixels = output.load()

        sin_time = time * 2 * math.pi  # precompute common value

        for x in range(self.size):
            for y in range(self.size):
                # Apply distortion
                xd, yd = self.apply_distortion(x, y, time)

                # Compute base spiral value
                spiral_val = self.generate_spirals(xd, yd, time)
                turbulence_val = self.generate_turbulence(xd, yd, time)
                shimmer_val = self.rng.uniform(0.0, self.shimmer) + math.sin(sin_time + ((x + y) / self.size) * math.pi) * self.shimmer

                # Combine effects
                n = spiral_val + turbulence_val + shimmer_val

                # Adjust spiral strength and offset, clamp to [0,1]
                n_adjusted = max(0.0, min(1.0, n * self.spiral_strength + self.spiral_offset))
                n_color = min(1.0, n_adjusted * 1.3)

                # Map to RGB
                r, g, b = self.color_map(n_color)
                a = int(self.alpha_base + n_adjusted * self.alpha_scale)

                # White-hot or random hotspot
                if n_adjusted > self.white_threshold and (self.rng.random() * 0.5 + 0.5) > 0.7:
                    r = g = b = a = self.white_alpha

                pixels[x, y] = (r, g, b, a)

        return output


    def generate_portal_sheet(self, output_file="nether_portal.png"):
        """Generate full animated portal sheet."""
        sheet = Image.new("RGBA", (self.size, self.size * self.frames))
        for i in range(self.frames):
            time = i / self.frames
            frame = self.setup_portal_sprite(time)
            sheet.paste(frame, (0, i * self.size))
        sheet.save(output_file)
        print(f"Saved {output_file} with {self.frames} frames")


# Example usage
if __name__ == "__main__":
    portal = SeamlessPlasmaPortalGenerator(
        size=16,
        frames=32,
        shimmer=0.05,
        white_threshold=0.85,
        turbulence_strength=0.05,
        hotspot_prob=0.02,
        distortion_strength=0.1,
        num_spiral_layers=4,
        base_color=(75,15,130),
    )
    portal.generate_portal_sheet()
