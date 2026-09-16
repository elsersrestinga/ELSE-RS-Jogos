import pygame, sys, random, asyncio
from jogo import Jogo

pygame.init()
pygame.mixer.init()

LARGURA_TELA = 750
ALTURA_TELA = 700
OFFSET = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

fonte = pygame.font.Font("Fonte/monogram.ttf", 40)
fim_de_jogo_surface = fonte.render("FIM DE JOGO", False, WHITE)
score_text_surface = fonte.render("SCORE", False, WHITE)
highscore_text_surface = fonte.render("HIGH-SCORE", False, WHITE)

tela = pygame.display.set_mode((LARGURA_TELA + OFFSET, ALTURA_TELA + 2 * OFFSET))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

jogo = Jogo(LARGURA_TELA, ALTURA_TELA, OFFSET)

ATIRAR_LASER = pygame.USEREVENT

NAVE_MISTERIO = pygame.USEREVENT + 1

async def main():
    intervalo = 300
    intetervalo_nave_misterio = random.randint(4000,8000)
    espera_tiro = 0
    espera_nave = 0
    musica_jogando_tocando = False
    musica_game_over_tocando = False
    pygame.mixer.music.set_volume(0.4)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ATIRAR_LASER and jogo.run:
                jogo.alien_atirar_laser()
            if event.type == NAVE_MISTERIO and jogo.run:
                jogo.criar_nave_misterio()
                intetervalo_nave_misterio = random.randint(4000,8000)
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and jogo.run == False:
            jogo.reset()
            tempo_atual = pygame.time.get_ticks

        #Carregando
        if jogo.run:
            jogo.nave_grupo.update()
            jogo.mover_aliens()
            jogo.aliens_lasers_grupo.update()
            jogo.nave_misterio_grupo.update()
            jogo.verificar_colisoes()
            jogo.proximo_nivel()
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - espera_tiro >= intervalo:
                tiro = pygame.event.Event(ATIRAR_LASER)
                pygame.event.post(tiro)
                espera_tiro = pygame.time.get_ticks()
            if tempo_atual - espera_nave >= intetervalo_nave_misterio:
                nave_misterio = pygame.event.Event(NAVE_MISTERIO)
                pygame.event.post(nave_misterio)
                espera_nave = pygame.time.get_ticks()
                intetervalo_nave_misterio += random.randint(4000,8000)

        #Desenhando
        tela.fill(BLACK)

        #UI
        pygame.draw.rect(tela, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(tela, WHITE, (25, 730), (775, 730), 3)

        level_formatado = str(jogo.level).zfill(2)
        level_surface = fonte.render(f"LEVEL {level_formatado}", False, WHITE)

        if jogo.run:
            tela.blit(level_surface, (570, 740, 50, 50))
            if not musica_jogando_tocando:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sons/SpaceSong.ogg")
                pygame.mixer.music.play(-1)
                musica_jogando_tocando = True
                musica_game_over_tocando = False
        else:
            tela.blit(fim_de_jogo_surface, (570, 740, 50, 50))
            if not musica_game_over_tocando:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sons/SpaceGameOver.ogg")
                pygame.mixer.music.play(-1)
                musica_game_over_tocando = True
                musica_jogando_tocando = False

        x = 50
        for live in range(jogo.vidas):
            tela.blit(jogo.nave_grupo.sprite.image, (x, 745))
            x += 50

        tela.blit(score_text_surface, (50, 15, 50, 50))
        formatado_score = str(jogo.score).zfill(5)
        score_surface = fonte.render(formatado_score, False, WHITE)
        tela.blit(score_surface, (50, 40, 50, 50))
        tela.blit(highscore_text_surface, (550, 15, 50, 50))
        formatado_highscore = str(jogo.highscore).zfill(5)
        highscore_surface = fonte.render(formatado_highscore, False, WHITE)
        tela.blit(highscore_surface, (625, 40, 50, 50))

        jogo.nave_grupo.draw(tela)
        jogo.nave_grupo.sprite.grupo_lasers.draw(tela)
        for defesa in jogo.defesas:
            defesa.grupo_blocos.draw(tela)
        jogo.aliens_grupo.draw(tela)
        jogo.aliens_lasers_grupo.draw(tela)
        jogo.nave_misterio_grupo.draw(tela)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())