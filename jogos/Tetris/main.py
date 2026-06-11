import pygame, sys, asyncio
from jogo import Jogo
from cores import Cores

pygame.init()
pygame.key.set_repeat(200, 50)
tela = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

async def main():
    tempo_ultima_descida = pygame.time.get_ticks()
    intervalo_descida = 500
    
    fonte_titulo = pygame.font.Font(None, 40)
    jogo = Jogo()
    while True:
        tempo_atual = pygame.time.get_ticks()
        if jogo.fim_de_jogo == False:
            if tempo_atual - tempo_ultima_descida > intervalo_descida:
                jogo.mover_baixo()
                tempo_ultima_descida = tempo_atual
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if jogo.fim_de_jogo == True:
                    jogo.fim_de_jogo = False
                    jogo.reset()
                if event.key == pygame.K_LEFT and jogo.fim_de_jogo == False:
                    jogo.mover_esq()
                if event.key == pygame.K_RIGHT and jogo.fim_de_jogo == False:
                    jogo.mover_dir()
                if event.key == pygame.K_DOWN and jogo.fim_de_jogo == False:
                    jogo.mover_baixo()
                    jogo.reler_pontos(0, 1)
                if event.key == pygame.K_UP and jogo.fim_de_jogo == False:
                    jogo.rotacao()

        plano_pontos_valor = fonte_titulo.render(str(jogo.pontos), True, Cores.branco)
        
        tela.fill(Cores.midnight_blue)
        plano_pontos = fonte_titulo.render("Pontos", True, Cores.branco)
        tela.blit(plano_pontos, (360, 20, 20, 50))
        plano_proximo = fonte_titulo.render("Próximo", True, Cores.branco)
        tela.blit(plano_proximo, (350, 180, 50, 50))

        plano_fim_de_jogo = fonte_titulo.render("Fim de Jogo", True, Cores.branco)
        if jogo.fim_de_jogo == True:
            tela.blit(plano_fim_de_jogo, (325, 450, 50, 50))

        pontos_retangulo = pygame.Rect(320, 55, 170, 60)
        pygame.draw.rect(tela, Cores.light_blue, pontos_retangulo, 0, 10)
        tela.blit(plano_pontos_valor, plano_pontos_valor.get_rect(centerx = pontos_retangulo.centerx, centery = pontos_retangulo.centery))
        proximo_retangulo = pygame.Rect(320, 215, 170, 180)
        pygame.draw.rect(tela, Cores.light_blue, proximo_retangulo, 0, 10)
        jogo.mostrar(tela)
        
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
            