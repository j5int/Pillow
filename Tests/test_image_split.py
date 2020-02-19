from PIL import Image, features

from .helper import PillowTestCase, assert_image_equal, hopper


class TestImageSplit(PillowTestCase):
    def test_split(self):
        def split(mode):
            layers = hopper(mode).split()
            return [(i.mode, i.size[0], i.size[1]) for i in layers]

        self.assertEqual(split("1"), [("1", 128, 128)])
        self.assertEqual(split("L"), [("L", 128, 128)])
        self.assertEqual(split("I"), [("I", 128, 128)])
        self.assertEqual(split("F"), [("F", 128, 128)])
        self.assertEqual(split("P"), [("P", 128, 128)])
        self.assertEqual(
            split("RGB"), [("L", 128, 128), ("L", 128, 128), ("L", 128, 128)]
        )
        self.assertEqual(
            split("RGBA"),
            [("L", 128, 128), ("L", 128, 128), ("L", 128, 128), ("L", 128, 128)],
        )
        self.assertEqual(
            split("CMYK"),
            [("L", 128, 128), ("L", 128, 128), ("L", 128, 128), ("L", 128, 128)],
        )
        self.assertEqual(
            split("YCbCr"), [("L", 128, 128), ("L", 128, 128), ("L", 128, 128)]
        )

    def test_split_merge(self):
        def split_merge(mode):
            return Image.merge(mode, hopper(mode).split())

        assert_image_equal(hopper("1"), split_merge("1"))
        assert_image_equal(hopper("L"), split_merge("L"))
        assert_image_equal(hopper("I"), split_merge("I"))
        assert_image_equal(hopper("F"), split_merge("F"))
        assert_image_equal(hopper("P"), split_merge("P"))
        assert_image_equal(hopper("RGB"), split_merge("RGB"))
        assert_image_equal(hopper("RGBA"), split_merge("RGBA"))
        assert_image_equal(hopper("CMYK"), split_merge("CMYK"))
        assert_image_equal(hopper("YCbCr"), split_merge("YCbCr"))

    def test_split_open(self):
        if features.check("zlib"):
            test_file = self.tempfile("temp.png")
        else:
            test_file = self.tempfile("temp.pcx")

        def split_open(mode):
            hopper(mode).save(test_file)
            with Image.open(test_file) as im:
                return len(im.split())

        self.assertEqual(split_open("1"), 1)
        self.assertEqual(split_open("L"), 1)
        self.assertEqual(split_open("P"), 1)
        self.assertEqual(split_open("RGB"), 3)
        if features.check("zlib"):
            self.assertEqual(split_open("RGBA"), 4)
