from PIL import Image, ImageDraw


class DrawDecisionTreeService:
    def __init__(self, tree, indent='', grafical=False, img_name="tree.jpg"):
        self.tree = tree
        self.indent = indent
        self.grafical = grafical
        self.img_name = img_name

    def call(self):
        if not self.grafical:
            return self.print_text_tree(self.tree, self.indent)

        return self.draw_tree(self.tree)

    def print_text_tree(self, tree, indent):
        """
        Recursively, call this method and print all node components into strout
        """
        if tree.results:
            print(str(dict(tree.results)))
        else:
            print("{}:{}? ".format(str(tree.col), str(tree.value)))

            # Print the branches
            print '{}T->'.format(indent),
            self.print_text_tree(tree.tb, indent + '  ')
            print '{}F->'.format(indent),
            self.print_text_tree(tree.fb, indent + '  ')

    def draw_tree(self, tree):
        w = self._get_width(tree) * 100
        h = self._get_depth(tree) * 100 + 120

        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self._draw_node(draw, tree, w / 2, 20)
        img.save(self.img_name, 'JPEG')

    def _get_width(self, tree):
        if not tree.tb and not tree.fb:
            return 1
        return self._get_width(tree.tb) + self._get_width(tree.fb)

    def _get_depth(self, tree):
        if not tree.tb and not tree.fb:
            return 0
        return max(self._get_depth(tree.tb), self._get_depth(tree.fb)) + 1

    def _draw_node(self, draw, tree, x, y):
        if not tree.results:
            w1 = self._get_width(tree.fb) * 100
            w2 = self._get_width(tree.tb) * 100

            # Determine the total space required by this node
            left = x - (w1 + w2) / 2
            right = x + (w1 + w2) / 2

            # Draw the condition string
            draw.text((x - 20, y - 10), str(tree.col) + ':' + str(tree.value), (0, 0, 0))

            # Draw links to the branches
            draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
            draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))

            # Draw the branch nodes
            self._draw_node(draw, tree.fb, left + w1 / 2, y + 100)
            self._draw_node(draw, tree.tb, right - w2 / 2, y + 100)
        else:
            txt = ' \n'.join(['%s:%d' % v for v in tree.results.items()])
            draw.text((x - 20, y), txt, (0, 0, 0))
