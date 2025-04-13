import pygame
import random
import numpy as np
from sklearn.cluster import SpectralCoclustering
from sklearn.metrics import normalized_mutual_info_score

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 900
COLORS = {
    'background': (240, 240, 250),
    'grid': (200, 200, 200),
    'user': (70, 130, 180),
    'item': (220, 20, 60),
    'interaction': [(255, 180, 180), (180, 255, 180), (180, 180, 255), (255, 255, 180), (255, 180, 255)],
    'cluster': [(45, 125, 210), (220, 60, 100), (80, 200, 120), (230, 165, 45), (160, 70, 220)]
}

# Simulation Parameters - Changed to 8x8
NUM_USERS = 8
NUM_ITEMS = 8
CLUSTERS = 3
ANIMATION_SPEED = 5  # Higher value = faster animation

class CoClusteringDemo:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Co-Clustering Recommendation Visualization")
        self.clock = pygame.time.Clock()
        
        # Initialize data
        self.users = [{'id': i, 'cluster': None} for i in range(NUM_USERS)]
        self.items = [{'id': i, 'cluster': None} for i in range(NUM_ITEMS)]
        self.interactions = np.zeros((NUM_USERS, NUM_ITEMS))
        self.show_clusters = False
        self.animating = False
        self.animation_frame = 0
        self.animation_max = 15  # Total animation frames
        self.animation_clusters = []
        self.recommendations = []
        self.selected_cluster = None  # Track selected cluster for filtering view
        
        # Generate random interactions with patterns
        self.generate_patterned_interactions()
        
        # Add fonts with reduced sizes
        self.title_font = pygame.font.SysFont('Arial', 42, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 32)
        self.label_font = pygame.font.SysFont('Arial', 22)
        self.info_font = pygame.font.SysFont('Arial', 20)

    def generate_patterned_interactions(self):
        # Clear existing interactions
        self.interactions = np.zeros((NUM_USERS, NUM_ITEMS))
        
        # Create cluster patterns (users in same clusters tend to like similar items)
        user_clusters = [i % CLUSTERS for i in range(NUM_USERS)]
        item_clusters = [i % CLUSTERS for i in range(NUM_ITEMS)]
        
        # Higher probability of interaction within the same cluster
        for i in range(NUM_USERS):
            for j in range(NUM_ITEMS):
                if user_clusters[i] == item_clusters[j]:
                    # Higher probability within cluster
                    if random.random() < 0.7:
                        self.interactions[i][j] = 1
                else:
                    # Lower probability outside cluster
                    if random.random() < 0.1:
                        self.interactions[i][j] = 1

    def draw_grid(self):
        cell_size = min(100, (WIDTH * 0.7) // NUM_ITEMS, (HEIGHT * 0.7) // NUM_USERS)
        start_x = (WIDTH - (NUM_ITEMS * cell_size)) // 2
        start_y = (HEIGHT - (NUM_USERS * cell_size)) // 2 + 50  # Adjusted to make room for title
        
        # Draw title
        title = self.title_font.render("Interactive Co-Clustering Visualization", True, (20, 20, 80))
        title_rect = title.get_rect(center=(WIDTH // 2, 40))
        self.screen.blit(title, title_rect)

        # Draw cluster backgrounds
        if self.show_clusters:
            for cluster_id in range(CLUSTERS):
                # Skip if filtering by a different cluster
                if self.selected_cluster is not None and cluster_id != self.selected_cluster:
                    continue
                    
                color = COLORS['cluster'][cluster_id % len(COLORS['cluster'])]
                
                # User clusters (left side)
                for user in [u for u in self.users if u['cluster'] == cluster_id]:
                    y = start_y + user['id'] * cell_size
                    pygame.draw.rect(self.screen, color, (start_x - 120, y, 120, cell_size))
                    # Add shine effect
                    pygame.draw.line(self.screen, (255, 255, 255, 128), 
                                    (start_x - 120, y), 
                                    (start_x - 105, y + 15), 3)
                
                # Item clusters (bottom)
                for item in [it for it in self.items if it['cluster'] == cluster_id]:
                    x = start_x + item['id'] * cell_size
                    pygame.draw.rect(self.screen, color, (x, start_y + NUM_USERS * cell_size, cell_size, 80))
                    # Add shine effect
                    pygame.draw.line(self.screen, (255, 255, 255, 128), 
                                    (x, start_y + NUM_USERS * cell_size), 
                                    (x + 15, start_y + NUM_USERS * cell_size + 15), 3)

        # Draw interactions
        for i in range(NUM_USERS):
            for j in range(NUM_ITEMS):
                # Skip if filtering by clusters and this cell doesn't belong to the selected cluster
                if (self.selected_cluster is not None and 
                    self.show_clusters and 
                    (self.users[i]['cluster'] != self.selected_cluster or 
                     self.items[j]['cluster'] != self.selected_cluster)):
                    # Draw faded/gray cell to indicate it's filtered out
                    x = start_x + j * cell_size
                    y = start_y + i * cell_size
                    pygame.draw.rect(self.screen, (235, 235, 235), (x, y, cell_size, cell_size))
                    continue
                
                x = start_x + j * cell_size
                y = start_y + i * cell_size
                
                # Cell background based on interaction
                if self.interactions[i][j]:
                    if self.show_clusters and self.users[i]['cluster'] is not None:
                        # Use cluster-based coloring
                        cluster_id = self.users[i]['cluster']
                        color_base = COLORS['cluster'][cluster_id % len(COLORS['cluster'])]
                        # Make it lighter for better visibility
                        color = tuple(min(c + 80, 255) for c in color_base)
                    else:
                        # Use regular interaction color
                        color = COLORS['interaction'][0]
                    
                    pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size))
                    
                    # Draw a little icon to show interaction
                    icon_size = cell_size // 3
                    pygame.draw.circle(self.screen, (50, 50, 50), 
                                      (x + cell_size//2, y + cell_size//2), 
                                      icon_size)
                    pygame.draw.circle(self.screen, (255, 255, 255), 
                                      (x + cell_size//2, y + cell_size//2), 
                                      icon_size - 2)
                else:
                    # Empty cell with very light background
                    pygame.draw.rect(self.screen, (245, 245, 245), (x, y, cell_size, cell_size))

        # Draw recommendations
        if self.show_clusters and self.recommendations:
            for rec in self.recommendations:
                user_id, item_id = rec
                
                # Skip if filtering by clusters and this recommendation doesn't match
                if (self.selected_cluster is not None and 
                    (self.users[user_id]['cluster'] != self.selected_cluster or 
                     self.items[item_id]['cluster'] != self.selected_cluster)):
                    continue
                
                x = start_x + item_id * cell_size
                y = start_y + user_id * cell_size
                
                # Draw recommendation highlight
                pygame.draw.rect(self.screen, (255, 215, 0, 100), 
                                (x, y, cell_size, cell_size), 3)
                
                # Draw star to indicate recommendation
                star_points = []
                center_x, center_y = x + cell_size//2, y + cell_size//2
                outer_radius = cell_size // 3
                inner_radius = cell_size // 6
                
                for i in range(10):
                    angle = (2 * np.pi * i) / 10
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    star_points.append((
                        center_x + radius * np.cos(angle),
                        center_y + radius * np.sin(angle)
                    ))
                
                pygame.draw.polygon(self.screen, (255, 215, 0), star_points)

        # Draw grid lines
        for i in range(NUM_USERS + 1):
            y = start_y + i * cell_size
            pygame.draw.line(self.screen, COLORS['grid'], (start_x, y), (start_x + NUM_ITEMS * cell_size, y), 2)
        for j in range(NUM_ITEMS + 1):
            x = start_x + j * cell_size
            pygame.draw.line(self.screen, COLORS['grid'], (x, start_y), (x, start_y + NUM_USERS * cell_size), 2)

        # Draw labels with abbreviated format
        for i in range(NUM_USERS):
            text = self.label_font.render(f'U{i+1}', True, (0, 0, 0))
            text_rect = text.get_rect(midright=(start_x - 10, start_y + i * cell_size + cell_size//2))
            self.screen.blit(text, text_rect)
            
            if self.show_clusters:
                cluster = self.users[i]['cluster']
                if cluster is not None:
                    text = self.info_font.render(f'C{cluster+1}', True, (255, 255, 255))
                    text_rect = text.get_rect(center=(start_x - 60, start_y + i * cell_size + cell_size//2))
                    self.screen.blit(text, text_rect)
                
        for j in range(NUM_ITEMS):
            text = self.label_font.render(f'I{j+1}', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(start_x + j * cell_size + cell_size//2, start_y + NUM_USERS * cell_size + 10))
            self.screen.blit(text, text_rect)
            
            if self.show_clusters:
                cluster = self.items[j]['cluster']
                if cluster is not None:
                    text = self.info_font.render(f'C{cluster+1}', True, (255, 255, 255))
                    text_rect = text.get_rect(center=(start_x + j * cell_size + cell_size//2, start_y + NUM_USERS * cell_size + 40))
                    self.screen.blit(text, text_rect)

    def advanced_cocluster(self):
        # Make sure we have enough interactions for clustering
        if np.sum(self.interactions) < CLUSTERS:
            # Not enough data for clustering
            error_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
            pygame.draw.rect(self.screen, (255, 220, 220), error_box)
            pygame.draw.rect(self.screen, (200, 0, 0), error_box, 3)
            
            error_text = self.button_font.render("Not enough data for clustering", True, (150, 0, 0))
            text_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            self.screen.blit(error_text, text_rect)
            
            help_text = self.info_font.render("Please add more interactions by clicking on the grid", True, (100, 0, 0))
            help_rect = help_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15))
            self.screen.blit(help_text, help_rect)
            
            pygame.display.flip()
            pygame.time.wait(2000)  # Display error for 2 seconds
            return

        # Use spectral co-clustering from scikit-learn
        model = SpectralCoclustering(n_clusters=CLUSTERS, random_state=0)
        try:
            model.fit(self.interactions)
            
            # Get row and column cluster assignments
            row_clusters = model.row_labels_
            col_clusters = model.column_labels_
            
            # Save results for animation
            self.animation_clusters = []
            for frame in range(self.animation_max + 1):
                user_clusters = []
                item_clusters = []
                for i in range(NUM_USERS):
                    if random.random() < frame / self.animation_max:
                        user_clusters.append(row_clusters[i])
                    else:
                        user_clusters.append(None)
                
                for j in range(NUM_ITEMS):
                    if random.random() < frame / self.animation_max:
                        item_clusters.append(col_clusters[j])
                    else:
                        item_clusters.append(None)
                
                self.animation_clusters.append({
                    'users': user_clusters,
                    'items': item_clusters
                })
            
            # Start animation
            self.animating = True
            self.animation_frame = 0
            self.selected_cluster = None  # Reset filter when redoing clustering
        
        except Exception as e:
            print(f"Error in clustering: {e}")
            # Display error message on screen
            error_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
            pygame.draw.rect(self.screen, (255, 220, 220), error_box)
            pygame.draw.rect(self.screen, (200, 0, 0), error_box, 3)
            
            error_text = self.button_font.render("Error in clustering", True, (150, 0, 0))
            text_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            self.screen.blit(error_text, text_rect)
            
            help_text = self.info_font.render("Try adding more diverse interactions", True, (100, 0, 0))
            help_rect = help_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15))
            self.screen.blit(help_text, help_rect)
            
            pygame.display.flip()
            pygame.time.wait(2000)  # Display error for 2 seconds

    def generate_recommendations(self):
        # Clear previous recommendations
        self.recommendations = []
        
        # Find potential recommendations based on cluster patterns
        for i in range(NUM_USERS):
            user_cluster = self.users[i]['cluster']
            if user_cluster is None:
                continue
                
            # Find items in the same cluster that the user hasn't interacted with yet
            for j in range(NUM_ITEMS):
                if self.interactions[i][j] == 0 and self.items[j]['cluster'] == user_cluster:
                    # This is a potential recommendation
                    self.recommendations.append((i, j))
        
        # Limit the number of recommendations to avoid cluttering
        if len(self.recommendations) > 10:
            self.recommendations = random.sample(self.recommendations, 10)

    def update_animation(self):
        if not self.animating:
            return
            
        if self.animation_frame < len(self.animation_clusters):
            clusters = self.animation_clusters[self.animation_frame]
            
            for i, user in enumerate(self.users):
                user['cluster'] = clusters['users'][i]
                
            for j, item in enumerate(self.items):
                item['cluster'] = clusters['items'][j]
                
            self.animation_frame += 1
        else:
            self.animating = False
            # Generate recommendations when animation finishes
            self.generate_recommendations()

    def draw_controls(self):
        # Draw control panel background
        panel_rect = pygame.Rect(WIDTH - 320, 100, 300, HEIGHT - 200)
        pygame.draw.rect(self.screen, (240, 240, 255), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 150), panel_rect, 3)
        
        # Panel title
        panel_title = self.button_font.render("Control Panel", True, (50, 50, 100))
        self.screen.blit(panel_title, (WIDTH - 245, 120))
        
        # Buttons
        button_y = 170
        button_height = 50  # Reduced height
        button_spacing = 15  # Reduced spacing
        
        # Cluster button
        cluster_button = pygame.Rect(WIDTH - 290, button_y, 240, button_height)
        cluster_color = (100, 150, 250) if not self.show_clusters else (120, 200, 120)
        pygame.draw.rect(self.screen, cluster_color, cluster_button)
        pygame.draw.rect(self.screen, (50, 50, 100), cluster_button, 3)
        
        # Gradient effect on button
        for i in range(10):
            pygame.draw.line(self.screen, 
                          (min(255, cluster_color[0] + i*10), 
                           min(255, cluster_color[1] + i*10), 
                           min(255, cluster_color[2] + i*10)),
                          (cluster_button.left, cluster_button.top + i*2),
                          (cluster_button.right, cluster_button.top + i*2), 1)
        
        text = self.button_font.render("Find Clusters", True, (255, 255, 255))
        text_rect = text.get_rect(center=cluster_button.center)
        self.screen.blit(text, text_rect)
        button_y += button_height + button_spacing
        
        # Randomize data button
        random_button = pygame.Rect(WIDTH - 290, button_y, 240, button_height)
        pygame.draw.rect(self.screen, (250, 150, 120), random_button)
        pygame.draw.rect(self.screen, (50, 50, 100), random_button, 3)
        
        # Gradient effect on button
        for i in range(10):
            pygame.draw.line(self.screen, 
                          (min(255, 250 + i*5), 
                           min(255, 150 + i*5), 
                           min(255, 120 + i*5)),
                          (random_button.left, random_button.top + i*2),
                          (random_button.right, random_button.top + i*2), 1)
        
        text = self.button_font.render("Randomize Data", True, (255, 255, 255))
        text_rect = text.get_rect(center=random_button.center)
        self.screen.blit(text, text_rect)
        button_y += button_height + button_spacing
        
        # Clear button
        clear_button = pygame.Rect(WIDTH - 290, button_y, 240, button_height)
        pygame.draw.rect(self.screen, (200, 100, 100), clear_button)
        pygame.draw.rect(self.screen, (50, 50, 100), clear_button, 3)
        
        # Gradient effect on button
        for i in range(10):
            pygame.draw.line(self.screen, 
                          (min(255, 200 + i*5), 
                           min(255, 100 + i*5), 
                           min(255, 100 + i*5)),
                          (clear_button.left, clear_button.top + i*2),
                          (clear_button.right, clear_button.top + i*2), 1)
        
        text = self.button_font.render("Clear All", True, (255, 255, 255))
        text_rect = text.get_rect(center=clear_button.center)
        self.screen.blit(text, text_rect)
        button_y += button_height + button_spacing

        # Information section
        info_y = button_y + 20
        
        info_title = self.label_font.render("How to Use:", True, (50, 50, 100))
        self.screen.blit(info_title, (WIDTH - 290, info_y))
        info_y += 25  # Reduced spacing
        
        instructions = [
            "• Click on grid to add/remove interactions",
            "• Press 'Find Clusters' to group similar",
            "  users and items together",
            "• Yellow stars show suggested items",
            "  for users based on their group"
        ]
        
        for line in instructions:
            text = self.info_font.render(line, True, (50, 50, 100))
            self.screen.blit(text, (WIDTH - 290, info_y))
            info_y += 22  # Reduced line spacing
        
        # Add filter info if clusters are shown
        if self.show_clusters:
            filter_text = self.info_font.render("• Click group buttons below to filter view", True, (50, 50, 100))
            self.screen.blit(filter_text, (WIDTH - 290, info_y))
            info_y += 30  # Extra space before cluster filter buttons
            
            # Add cluster filter buttons
            filter_label = self.info_font.render("Filter by Group:", True, (50, 50, 100))
            self.screen.blit(filter_label, (WIDTH - 290, info_y))
            info_y += 25
            
            # All clusters button
            all_btn_width = 60
            all_btn = pygame.Rect(WIDTH - 290, info_y, all_btn_width, 30)
            all_color = (130, 130, 180) if self.selected_cluster is None else (180, 180, 200)
            pygame.draw.rect(self.screen, all_color, all_btn)
            pygame.draw.rect(self.screen, (50, 50, 100), all_btn, 2)
            
            all_text = self.info_font.render("All", True, (255, 255, 255))
            all_text_rect = all_text.get_rect(center=all_btn.center)
            self.screen.blit(all_text, all_text_rect)
            
            # Individual cluster buttons
            for c in range(CLUSTERS):
                btn_width = 50
                c_btn = pygame.Rect(WIDTH - 290 + all_btn_width + 10 + (btn_width + 5) * c, info_y, btn_width, 30)
                c_color = COLORS['cluster'][c % len(COLORS['cluster'])] if self.selected_cluster == c else (180, 180, 200)
                pygame.draw.rect(self.screen, c_color, c_btn)
                pygame.draw.rect(self.screen, (50, 50, 100), c_btn, 2)
                
                c_text = self.info_font.render(f"C{c+1}", True, (255, 255, 255))
                c_text_rect = c_text.get_rect(center=c_btn.center)
                self.screen.blit(c_text, c_text_rect)
            
            info_y += 40
        
        # Stats display - only show when clusters are active
        if self.show_clusters:
            stats_y = info_y + 15  # Reduced spacing
            
            # Simple explanation box
            explanation_box = pygame.Rect(WIDTH - 290, stats_y, 240, 65)
            pygame.draw.rect(self.screen, (230, 230, 245), explanation_box)
            pygame.draw.rect(self.screen, (80, 80, 120), explanation_box, 2)
            
            explain_title = self.label_font.render("What's Happening:", True, (50, 50, 100))
            self.screen.blit(explain_title, (WIDTH - 280, stats_y + 5))
            
            explain_text = self.info_font.render("Users and items with similar", True, (60, 60, 100))
            self.screen.blit(explain_text, (WIDTH - 280, stats_y + 30))
            explain_text2 = self.info_font.render("patterns are grouped by color", True, (60, 60, 100))
            self.screen.blit(explain_text2, (WIDTH - 280, stats_y + 45))
            
            stats_y += 80
            
            # Count interactions by cluster
            cluster_stats = {}
            for i in range(NUM_USERS):
                for j in range(NUM_ITEMS):
                    if (self.interactions[i][j] == 1 and 
                        self.users[i]['cluster'] is not None and 
                        self.items[j]['cluster'] is not None):
                        cluster_pair = (self.users[i]['cluster'], self.items[j]['cluster'])
                        if cluster_pair not in cluster_stats:
                            cluster_stats[cluster_pair] = 0
                        cluster_stats[cluster_pair] += 1
            
            # Show recommendations summary
            if self.recommendations:
                # Filter recommendations if we're showing a specific cluster
                visible_recs = self.recommendations
                if self.selected_cluster is not None:
                    visible_recs = [rec for rec in self.recommendations 
                                   if self.users[rec[0]]['cluster'] == self.selected_cluster 
                                   and self.items[rec[1]]['cluster'] == self.selected_cluster]
                
                if visible_recs:  # Only show if we have visible recommendations
                    rec_box = pygame.Rect(WIDTH - 290, stats_y, 240, 35)
                    pygame.draw.rect(self.screen, (255, 245, 225), rec_box)
                    pygame.draw.rect(self.screen, (255, 180, 0), rec_box, 2)
                    
                    rec_text = self.info_font.render(f"Found {len(visible_recs)} recommendations", 
                                                True, (180, 100, 0))
                    self.screen.blit(rec_text, (WIDTH - 280, stats_y + 12))
                    stats_y += 45
            
            # Group information
            groups_title = self.label_font.render("Group Overview:", True, (50, 50, 100))
            self.screen.blit(groups_title, (WIDTH - 290, stats_y))
            stats_y += 25
            
            # Draw colored group indicators
            for c in range(CLUSTERS):
                # Skip if filtering by a different cluster
                if self.selected_cluster is not None and c != self.selected_cluster:
                    continue
                    
                group_box = pygame.Rect(WIDTH - 290, stats_y, 240, 30)
                color = COLORS['cluster'][c % len(COLORS['cluster'])]
                light_color = tuple(min(c + 40, 255) for c in color)
                
                # Create gradient background
                pygame.draw.rect(self.screen, light_color, group_box)
                for i in range(15):
                    pygame.draw.line(self.screen, 
                                  color, 
                                  (group_box.left, group_box.top + i), 
                                  (group_box.right, group_box.top + i), 1)
                
                pygame.draw.rect(self.screen, color, group_box, 2)
                
                # Count users and items in this group
                users_in_group = sum(1 for user in self.users if user['cluster'] == c)
                items_in_group = sum(1 for item in self.items if item['cluster'] == c)
                
                group_text = self.info_font.render(f"Group {c+1}: {users_in_group} users, {items_in_group} items", 
                                              True, (255, 255, 255))
                self.screen.blit(group_text, (WIDTH - 280, stats_y + 7))
                stats_y += 35

    def clear_interactions(self):
        self.interactions = np.zeros((NUM_USERS, NUM_ITEMS))
        self.show_clusters = False
        for user in self.users:
            user['cluster'] = None
        for item in self.items:
            item['cluster'] = None
        self.recommendations = []
        self.selected_cluster = None

    def run(self):
        running = True
        while running:
            self.screen.fill(COLORS['background'])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    
                    # Calculate cell size and grid positioning
                    cell_size = min(100, (WIDTH * 0.7) // NUM_ITEMS, (HEIGHT * 0.7) // NUM_USERS)
                    start_x = (WIDTH - (NUM_ITEMS * cell_size)) // 2
                    start_y = (HEIGHT - (NUM_USERS * cell_size)) // 2 + 50
                    
                    # Check if click was inside the grid
                    grid_x = x - start_x
                    grid_y = y - start_y
                    
                    if 0 <= grid_x < NUM_ITEMS * cell_size and 0 <= grid_y < NUM_USERS * cell_size:
                        # Convert to grid coordinates
                        col = int(grid_x // cell_size)
                        row = int(grid_y // cell_size)
                        
                        # Ensure we're within bounds
                        if 0 <= row < NUM_USERS and 0 <= col < NUM_ITEMS:
                            # Toggle interaction (This is safer than the previous code)
                            current_value = self.interactions[row][col]
                            self.interactions[row][col] = 0 if current_value > 0 else 1
                            
                            # Reset clusters when data changes
                            if self.show_clusters:
                                self.show_clusters = False
                                for user in self.users:
                                    user['cluster'] = None
                                for item in self.items:
                                    item['cluster'] = None
                                self.recommendations = []
                                self.selected_cluster = None
                    
                    # Check cluster button click
                    cluster_button = pygame.Rect(WIDTH - 290, 170, 240, 50)



                    if cluster_button.collidepoint(x, y):
                        self.show_clusters = True
                        self.advanced_cocluster()
                    
                    # Check randomize button click
                    random_button = pygame.Rect(WIDTH - 290, 170 + 50 + 15, 240, 50)
                    if random_button.collidepoint(x, y):
                        self.generate_patterned_interactions()
                        # Reset clusters
                        self.show_clusters = False
                        for user in self.users:
                            user['cluster'] = None
                        for item in self.items:
                            item['cluster'] = None
                        self.recommendations = []
                        self.selected_cluster = None
                    
                    # Check clear button click
                    clear_button = pygame.Rect(WIDTH - 290, 170 + 2*(50 + 15), 240, 50)
                    if clear_button.collidepoint(x, y):
                        self.clear_interactions()
                    
                    # Check cluster filter buttons if clusters are shown
                    if self.show_clusters:
                        button_y = 170 + 3*(50 + 15) + 20 + 25 + 30 + 77
                        
                        # "All" button
                        all_btn_width = 60
                        all_btn = pygame.Rect(WIDTH - 290, button_y, all_btn_width, 30)
                        if all_btn.collidepoint(x, y):
                            self.selected_cluster = None
                        
                        # Individual cluster buttons
                        for c in range(CLUSTERS):
                            btn_width = 50
                            c_btn = pygame.Rect(WIDTH - 290 + all_btn_width + 10 + (btn_width + 5) * c, button_y, btn_width, 30)
                            if c_btn.collidepoint(x, y):
                                # Toggle the filter
                                if self.selected_cluster == c:
                                    self.selected_cluster = None
                                else:
                                    self.selected_cluster = c
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.show_clusters:
                            self.show_clusters = True
                            self.advanced_cocluster()
                        else:
                            self.show_clusters = False
                            for user in self.users:
                                user['cluster'] = None
                            for item in self.items:
                                item['cluster'] = None
                            self.recommendations = []
                            self.selected_cluster = None
                    
                    if event.key == pygame.K_r:
                        self.generate_patterned_interactions()
                        # Reset clusters
                        self.show_clusters = False
                        for user in self.users:
                            user['cluster'] = None
                        for item in self.items:
                            item['cluster'] = None
                        self.recommendations = []
                        self.selected_cluster = None
                    
                    if event.key == pygame.K_c:
                        self.clear_interactions()
                    
                    # Number keys 1-3 to filter by cluster
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        if self.show_clusters:
                            cluster_num = event.key - pygame.K_1  # Convert to 0-based index
                            if cluster_num < CLUSTERS:
                                # Toggle the filter
                                if self.selected_cluster == cluster_num:
                                    self.selected_cluster = None
                                else:
                                    self.selected_cluster = cluster_num

            # Update animation if needed
            if self.animating:
                self.update_animation()

            self.draw_grid()
            self.draw_controls()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    demo = CoClusteringDemo()
    demo.run()
