from manim import *
import numpy as np
from colour import Color

class EnhancedTreeNode:
    def __init__(self, value, position=ORIGIN):
        self.value = value
        self.position = position
        self.left = None
        self.right = None

class PureVisualTreeAnimation(Scene):
    def construct(self):
        # Modern, vibrant color palette
        self.camera.background_color = "#0A192F"  # Deep navy background
        
        # Enhanced color scheme with more vibrant colors
        self.colors = {
            'node_fill': "#233554",          # Deep blue for nodes
            'node_stroke': "#64FFDA",        # Bright teal for borders
            'text': "#E6F1FF",              # Bright white for text
            'highlight': "#FF5D8F",         # Vibrant pink for highlights
            'success': "#64FFDA",           # Teal for success states
            'edge': "#8892B0",              # Light blue-gray for edges
            'glow': "#64FFDA",              # Teal glow
            'accent': "#FFA7C4"             # Soft pink accent
        }

        # Initialize scene components
        self.tree = self.create_enhanced_tree()
        self.tree_mobjects = {}
        self.edges = []
        self.sum_labels = {}
        
        # Create and animate the enhanced tree visualization
        self.create_pure_visual_tree(self.tree, UP * 2, 3, 1.5)
        self.animate_enhanced_tree_creation()
        
        # Perform and visualize the sum calculation with enhanced effects
        total_sum = self.animate_pure_visual_sum(self.tree)
        
        self.wait(2)

    def create_enhanced_tree(self):
        # Creating a visually balanced tree
        root = EnhancedTreeNode(25)
        root.left = EnhancedTreeNode(12)
        root.right = EnhancedTreeNode(38)
        root.left.left = EnhancedTreeNode(6)
        root.left.right = EnhancedTreeNode(18)
        root.right.left = EnhancedTreeNode(30)
        root.right.right = EnhancedTreeNode(44)
        return root

    def create_pure_visual_tree(self, node, position, x_spread, y_spread):
        if node is None:
            return

        # Enhanced node design with multiple layers for depth
        main_circle = Circle(
            radius=0.4,
            stroke_width=3,
            stroke_color=self.colors['node_stroke'],
            fill_color=self.colors['node_fill'],
            fill_opacity=0.95
        )
        
        # Multiple glow layers for enhanced depth effect
        glow_layers = VGroup(*[
            Circle(
                radius=0.4 + (i * 0.08),
                stroke_width=2,
                stroke_color=self.colors['glow'],
                stroke_opacity=0.2 - (i * 0.05)
            )
            for i in range(3)
        ])
        
        # Enhanced value text with better visibility
        value = Text(
            str(node.value),
            color=self.colors['text'],
            font="Sans Serif",
            weight="BOLD"
        ).scale(0.7)
        
        # Group all elements
        node_group = VGroup(main_circle, glow_layers, value)
        node_group.move_to(position)
        self.tree_mobjects[id(node)] = node_group
        node.position = position

        # Create enhanced curved edges with gradients
        if node.left:
            left_pos = position + DOWN * y_spread + LEFT * x_spread
            edge = CurvedArrow(
                start_point=position,
                end_point=left_pos,
                angle=-0.3,
                stroke_width=3,
                stroke_opacity=0.8,
                color=self.colors['edge']
            )
            self.edges.append(edge)
            self.create_pure_visual_tree(node.left, left_pos, x_spread/2, y_spread)

        if node.right:
            right_pos = position + DOWN * y_spread + RIGHT * x_spread
            edge = CurvedArrow(
                start_point=position,
                end_point=right_pos,
                angle=0.3,
                stroke_width=3,
                stroke_opacity=0.8,
                color=self.colors['edge']
            )
            self.edges.append(edge)
            self.create_pure_visual_tree(node.right, right_pos, x_spread/2, y_spread)

    def animate_enhanced_tree_creation(self):
        # Animate edges with cascading effect and glows
        for i, edge in enumerate(self.edges):
            self.play(
                Create(edge),
                run_time=0.4,
                rate_func=smooth
            )
            
            # Add subtle pulse to the edge
            self.play(
                edge.animate.set_stroke(opacity=0.4),
                edge.animate.set_stroke(opacity=0.8),
                run_time=0.2
            )
        
        # Animate nodes with enhanced effects
        for node in self.tree_mobjects.values():
            # Create node with ripple effect
            self.play(
                DrawBorderThenFill(node[0]),
                FadeIn(node[1], scale=1.2),
                FadeIn(node[2], shift=DOWN * 0.2),
                run_time=0.5
            )
            
            # Add pulsing glow effect
            self.play(
                node[1].animate.scale(1.1).set_opacity(0.3),
                node[1].animate.scale(1/1.1).set_opacity(0.2),
                run_time=0.3
            )

    def animate_pure_visual_sum(self, node, run_time=1.0):
        if node is None:
            return 0

        node_vis = self.tree_mobjects[id(node)]
        
        # Enhanced highlight animation
        self.play(
            node_vis[1].animate.set_color(self.colors['highlight']),
            node_vis[0].animate.set_fill(self.colors['highlight'], opacity=0.3),
            Flash(
                node_vis[0],
                color=self.colors['highlight'],
                line_length=0.2,
                flash_radius=0.4,
                num_lines=12,
                run_time=0.5
            ),
            run_time=run_time/2
        )

        # Recursive sum calculation with visual feedback
        left_sum = self.animate_pure_visual_sum(node.left, run_time/1.2)
        right_sum = self.animate_pure_visual_sum(node.right, run_time/1.2)
        current_sum = node.value + left_sum + right_sum

        # Create enhanced sum visualization
        sum_circle = Circle(
            radius=0.2,
            stroke_width=2,
            stroke_color=self.colors['success'],
            fill_color=self.colors['node_fill'],
            fill_opacity=0.9
        )
        
        sum_text = Text(
            str(current_sum),
            color=self.colors['success'],
            font="Sans Serif",
            weight="BOLD"
        ).scale(0.4)
        
        sum_group = VGroup(sum_circle, sum_text)
        sum_group.next_to(node_vis, UP, buff=0.2)
        
        # Animate sum calculation with enhanced effects
        self.play(
            FadeIn(sum_group, shift=DOWN * 0.2),
            node_vis[0].animate.set_fill(self.colors['success'], opacity=0.2),
            node_vis[1].animate.set_color(self.colors['success']),
            Flash(
                sum_circle,
                color=self.colors['success'],
                line_length=0.1,
                flash_radius=0.2,
                num_lines=8,
                run_time=0.5
            ),
            run_time=run_time
        )
        
        # Clean up previous sum visualization
        if id(node) in self.sum_labels:
            self.play(
                FadeOut(self.sum_labels[id(node)]),
                run_time=run_time/2
            )
        self.sum_labels[id(node)] = sum_group
        
        return current_sum

if __name__ == "__main__":
    scene = PureVisualTreeAnimation()