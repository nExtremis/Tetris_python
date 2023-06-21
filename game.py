from grid import Grid
from blocks import *
import random
import pygame
import sys
from colors import * 
import sqlite3

POINTS_PER_LEVEL = 200
GAME_UPDATE = pygame.USEREVENT
class Game:
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.level = 1
		self.game_over = False
		self.show_menu_message = False
		self.in_main_menu = True
		self.is_playing = False
		self.title_font = pygame.font.Font(None, 40)
		self.colores = Colors() 
		self.score = 0
		self.score_surface = self.title_font.render("Score", True, Colors.white)
		self.score_rect = pygame.Rect(320, 55, 170, 60)
		self.next_surface = self.title_font.render("Next", True, Colors.white)
		self.next_rect = pygame.Rect(320, 215, 170, 180)
		self.font_path = "./font/font.ttf"
		self.title_font_score = pygame.font.Font(self.font_path, 40)
		self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
		self.bandera_musica =  False
		self.background_image_1 = pygame.image.load("./img/sky_1.png")
		self.background_scaled_1 = pygame.transform.scale(self.background_image_1,(self.grid.num_cols*self.grid.cell_size,self.grid.num_rows*self.grid.cell_size))
		self.background_image_2 = pygame.image.load("./img/sky_2.png")
		self.background_scaled_2 = pygame.transform.scale(self.background_image_2,(self.grid.num_cols*self.grid.cell_size,self.grid.num_rows*self.grid.cell_size))
		self.background_image_3 = pygame.image.load("./img/sky_3.png")
		self.background_scaled_3 = pygame.transform.scale(self.background_image_3,(self.grid.num_cols*self.grid.cell_size,self.grid.num_rows*self.grid.cell_size))
		self.background_image_4 = pygame.image.load("./img/sky_4.png")
		self.background_scaled_4 = pygame.transform.scale(self.background_image_4,(self.grid.num_cols*self.grid.cell_size,self.grid.num_rows*self.grid.cell_size))

		self.clock = pygame.time.Clock()
		self.game_update_interval = 200
		
		
	def mostrar_fondo(self,screen):
		if self.level == 1:
			return screen.blit(self.background_scaled_1,(11,11))	
		elif self.level == 1:
			return screen.blit(self.background_scaled_2,(11,11))
		elif self.level == 1:
			return screen.blit(self.background_scaled_3,(11,11))	
		else:
			return screen.blit(self.background_scaled_4,(11,11))			
    		
		
	def score_sqlite(self,nick):
		self.conn = sqlite3.connect("puntuaciones.db")
		self.cursor = self.conn.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS puntuaciones (nick TEXT, score INTEGER)")
		self.cursor.execute("INSERT INTO puntuaciones (nick, score) VALUES (?, ?)", (nick, self.score))					
		self.conn.commit()
		self.conn.close()


	def ingresar_nick(self,screen, screen_width):
		font_path = "./font/font.ttf"
		font = pygame.font.Font(font_path, 30)

		nick = ""

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return ""  # Salir de la función y volver al juego principal
					elif event.key == pygame.K_BACKSPACE:
						nick = nick[:-1]
					elif event.key >= pygame.K_a and event.key <= pygame.K_z:
						if len(nick) < 3:
							letter = chr(event.key).upper()
							nick += letter

			screen.fill((0, 0, 0))

			title_font = pygame.font.Font(font_path, 40)
			title_surface = title_font.render("Ingrese su nick", True, (255, 255, 255))
			title_rect = title_surface.get_rect(center=(screen_width // 2, 50))
			screen.blit(title_surface, title_rect)

			nick_surface = font.render(nick, True, (255, 255, 255))
			nick_rect = nick_surface.get_rect(center=(screen_width // 2, 120))
			screen.blit(nick_surface, nick_rect)

			pygame.display.flip()

			if len(nick) == 3:
				return nick


	def mostrar_ranking(self,screen,screen_width):
		# Conexión a la base de datos
		self.conn = sqlite3.connect("puntuaciones.db")
		self.cursor = self.conn.cursor()

		# Realizar consulta a la base de datos
		self.cursor.execute("SELECT nick, score FROM puntuaciones ORDER BY score DESC LIMIT 10")
		puntuaciones = self.cursor.fetchall()

		# Cerrar la conexión a la base de datos
		self.conn.close()

		# Limpiar la pantalla y mostrar los puntajes
		screen.fill((0, 0, 0))

		font_path = "./font/font.ttf"
		font = pygame.font.Font(font_path, 30)

		title_font = pygame.font.Font(font_path, 40)
		title_surface = title_font.render("Top 10 Puntajes", True, (255, 255, 255))
		title_rect = title_surface.get_rect(center=(screen_width // 2, 50))
		screen.blit(title_surface, title_rect)
		y = 120
		for i, (nick, score) in enumerate(puntuaciones, start=1):
			text = f"{i}. {nick}: {score}"
			text_surface = font.render(text, True, (255, 255, 255))
			text_rect = text_surface.get_rect(midtop=(screen_width // 2, y))
			screen.blit(text_surface, text_rect)
			y += 30

		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return
	def dibujar_score(self,screen,score_value_surface):
		pygame.draw.rect(screen, self.colores.light_blue, self.score_rect, 0, 10)
		screen.blit(score_value_surface, score_value_surface.get_rect(centerx = self.score_rect.centerx, 
			centery = self.score_rect.centery))	
	def dibujar_proxima_figura(self,screen):
		pygame.draw.rect(screen, Colors.light_blue, self.next_rect, 0, 10)
		
	def main_menu(self,screen,screen_width):
		menu_options = ["Jugar", "Ranking", "Salir"]
		selected_option = 0  # Índice de la opción seleccionada

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						selected_option = (selected_option - 1) % len(menu_options)
					elif event.key == pygame.K_DOWN:
						selected_option = (selected_option + 1) % len(menu_options)
					elif event.key == pygame.K_RETURN:
						if selected_option == 0:
							self.is_playing = True
							self.bandera_musica = False
							self.reset()
							
							return
						elif selected_option == 1:
							self.mostrar_ranking(screen,screen_width)
						elif selected_option == 2:
							pygame.quit()
							sys.exit()

			# Limpiar la pantalla y dibujar el menú principal
			screen.fill((0, 0, 0))
			for i, option in enumerate(menu_options):
				color = (255, 255, 255) if i == selected_option else (128, 128, 128)
				text_surface = self.title_font_score.render(option, True, color)
				text_rect = text_surface.get_rect(center=(screen_width // 2, 200 + i * 100))
				screen.blit(text_surface, text_rect)

			pygame.display.update()
			pygame.display.flip()


	def setup_timer(self):
        #Configura el temporizador y el intervalo de tiempo para el evento GAME_UPDATE
		pygame.time.set_timer(GAME_UPDATE, self.game_update_interval)

	def get_game_update_interval(self):
		if self.level == 2:
			return 150
		elif self.level == 3:
			return 100
		elif self.level == 4:
			return 70
		else:
			return 200  # Intervalo predeterminado si el nivel no coincide con ninguno de los casos anteriores
	
	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		elif lines_cleared == 4:
			self.score += 600
		elif lines_cleared == 5:
			self.score += 600	
		self.score += move_down_points

		if self.score >= self.level * POINTS_PER_LEVEL:
			self.level += 1
			
			if self.bandera_musica == True:
				pygame.mixer.music.stop()
				self.bandera_musica = False
				
				if self.bandera_musica == False and self.level==2:
					pygame.mixer.music.load("Sounds/Spectrum-Holobyte-Tetris-Color.ogg")
					pygame.mixer.music.play(-1)
					self.bandera_musica = True
				elif self.bandera_musica == False and self.level==3:
					pygame.mixer.music.load("Sounds/Gameboy-Music-Tetris-Music-A.ogg")
					pygame.mixer.music.play(-1)
					self.bandera_musica = True
				elif self.bandera_musica == False and self.level==4:
					pygame.mixer.music.load("Sounds/Tetris-99-Main-Theme.ogg")
					pygame.mixer.music.play(-1)
					self.bandera_musica = True

	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)
		
		if self.next_block.id == 3:
			self.next_block.draw(screen, 330, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 330, 280)
		else:
    		
			self.next_block.draw(screen, 300, 270)