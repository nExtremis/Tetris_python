import pygame,sys
from game import *
from colors import Colors
import sqlite3
conn = sqlite3.connect("puntuaciones.db")
cursor = conn.cursor()

pygame.init()

game = Game()
game_over_surface = game.title_font.render("GAME OVER", True, Colors.white)
game_over_menu = game.title_font.render("Presiona Enter para ir al menu principal", True, Colors.white)
game_menu_rect = game_over_menu.get_rect(center=(500 // 2, 480 // 2))

screen = pygame.display.set_mode((500, 480))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

GAME_UPDATE = pygame.USEREVENT
GAME_INVERTAL = 200
pygame.time.set_timer(GAME_UPDATE, GAME_INVERTAL) 

game.main_menu(screen,500)	

while True:
	print(game.bandera_musica)
	if game.bandera_musica == False and game.level==1:
		pygame.mixer.music.load("Sounds/music_1.ogg")
		pygame.mixer.music.play(-1)
		game.bandera_musica = True
			
	
	if game.is_playing:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if game.game_over == True:
					game.game_over = False
					game.reset()
				if event.key == pygame.K_LEFT and game.game_over == False:
					game.move_left()
				if event.key == pygame.K_RIGHT and game.game_over == False:
					game.move_right()
				if event.key == pygame.K_DOWN and game.game_over == False:
					game.move_down()
					game.update_score(0, 1)
				if event.key == pygame.K_UP and game.game_over == False:
					game.rotate()
			if event.type == GAME_UPDATE and game.game_over == False:
				
				GAME_UPDATE_INTERVAL = game.get_game_update_interval()
				pygame.time.set_timer(GAME_UPDATE, GAME_UPDATE_INTERVAL)	
				game.move_down()
		#Drawing

		score_value_surface = game.title_font_score.render(str(game.score), True, Colors.white)

		screen.fill(Colors.dark_blue)
		game.mostrar_fondo(screen)
		#screen.blit(game.background_scaled,(11,11))
		screen.blit(game.score_surface, (365, 20, 50, 50))
		screen.blit(game.next_surface, (365, 180, 50, 50))

		if game.game_over == True:
			screen.blit(game_over_surface, (320, 450, 50, 50))
			nick = game.ingresar_nick(screen, 500)
			game.score_sqlite(nick)
			game.mostrar_ranking(screen,500)
			GAME_UPDATE_INTERVAL = 200
			#screen.blit(game_over_menu,game_menu_rect)
			game.is_playing = False
			game.game_over = False
			pygame.mixer.music.stop()
			game.bandera_musica = False

			
		game.dibujar_score(screen,score_value_surface)
		game.dibujar_proxima_figura(screen)
		game.draw(screen)
	else:
		game.main_menu(screen,500)

	pygame.display.update()
	
	clock.tick(10)
	