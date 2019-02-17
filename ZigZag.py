import sys
import pygame
import random

class Difficult():
    def __init__(self):
        self.list = []



    def difficult(self):

        # Инициализируем движок
        pygame.init()

        # Определяем цвета

        black     = (  0,   0,   0)   # черный
        green     = (  0, 128,   0)   # зеленый
        red       = (255,   0,   0)   # красный
        white     = (220, 255, 255)   # белый
        yellow    = (255, 255,   0)   # желтый


        # Задаем ширину и высоту экрана
        size = [500,400]
        screen = pygame.display.set_mode(size)


        pygame.display.set_caption("Выбор уровня сложности")

        done=False
        clock=pygame.time.Clock()

        # Основной цикл программы

        while done==False:

            for event in pygame.event.get():

                # Выясняем какая именно кнопка была нажата

                if event.type ==pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:


                    if event.key == pygame.K_1:
                        A = 1
                        done = True
                    elif event.key == pygame.K_2:
                        A = 2
                        done = True
                    elif event.key == pygame.K_3:
                        A = 3
                        done = True
                    else:
                        continue

                    screen.fill(white)


                    return A


            fontObj = pygame.font.Font('freesansbold.ttf', 30)
            textSurfaceObj = fontObj.render('Выбор уровня сложности:', True, black, white)
            textN = fontObj.render('Новичок — Нажми 1', True, green, white)
            textL = fontObj.render('Любитель — Нажми 2', True, yellow, white)
            textP = fontObj.render('Профессионал — Нажми 3', True, red, white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (250, 50)

            textRectN = textN.get_rect()
            textRectN.center = (250, 200)

            textRectL = textL.get_rect()
            textRectL.center = (250, 250)

            textRectP = textP.get_rect()
            textRectP.center = (250, 300)

            screen.fill(white)
            screen.blit(textSurfaceObj, textRectObj)
            screen.blit(textN, textRectN)
            screen.blit(textL, textRectL)
            screen.blit(textP, textRectP)


            pygame.display.flip()

        pygame.quit()



cl = Difficult()
D = cl.difficult()



"""
Настройки размера окна и скорости игры
"""


WIDTH = 480
HEIGHT = 480

if D == 1:
	FPS = 30
elif  D == 2:
	FPS = 60
elif  D == 3:
	FPS = 90

FPSCLOCK = pygame.time.Clock()

size = [WIDTH,HEIGHT]
screen = pygame.display.set_mode(size)
background = pygame.Surface(size)


"""
Используемые цвета
"""
BACKGROUND = (220, 255, 255)
ROAD = (0, 230, 230)
LEFTROAD = (0, 200, 200)
RIGHTROAD = (0, 200, 200)
TEXT = (30, 30, 30)


"""
Настройка краев
"""
LeftLimit = (WIDTH)//3
RightLimit = WIDTH - LeftLimit

"""
Добавление дорог
"""
class Main():
    def __init__(self):
        self.list = []


    def addRoad(self, ox, oy, road):
        factor = segFactors[random.randrange(len(segFactors))]
        if road == 1 and (ox + speedFactor*factor*segLen) < RightLimit:
            ox += speedFactor*factor*segLen
            oy -= factor*segLen
        elif (ox - speedFactor*factor*segLen) > LeftLimit:
            ox -= speedFactor*factor*segLen
            oy -= factor*segLen
        else:
            ox += speedFactor*factor*segLen
            oy -= factor*segLen
        return [ox, oy]

    def Roads(self, ballRect, road):

        ox = ballRect.left
        oy = ballRect.top + ballRect.height
        roadPoints.append([ox, oy])
        ox += speedFactor*50
        oy -= 50
        roadPoints.append([ox, oy])

        while oy >= -(HEIGHT):

            tmp = ma.addRoad(ox, oy, road)
            ox = tmp[0]
            oy = tmp[1]
            roadPoints.append(tmp)
            road = 1 - road

        return road

    def waitForKeyPress(self):
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return event.key




    def gameOver(self, ballRect, roadWidth):
        roadPointsLen = len(roadPoints) - 1
        i = 0
        while i < roadPointsLen-1:


            if ballRect.centery <= roadPoints[i][1] and ballRect.centery > roadPoints[i+1][1]:

                xcord = 0

                if roadPoints[i][0] < roadPoints[i+1][0]:
                    xcord = roadPoints[i][0] + speedFactor*(roadPoints[i][1] - ballRect.centery)
                else:
                    xcord = roadPoints[i][0] - speedFactor*(roadPoints[i][1] - ballRect.centery)

                leftLimit = xcord - roadWidth//2
                rightLimit = xcord + roadWidth//2

                if ballRect.centerx < leftLimit or ballRect.centerx > rightLimit:
                    return True

                break
            i += 1
        return False



    def playGame(self):

        pygame.init()

        font = pygame.font.get_default_font()
        font40=pygame.font.SysFont(font,30)
        font15=pygame.font.SysFont(font,18)

        score = 0
        global highScore

        pygame.mixer.music.load('data\music.mp3')
        pygame.mixer.music.play()
        pygame.time.delay(20)

        """
        Загрузка мяча
        """

        ball = pygame.image.load("data/ball.png")
        ballRect = ball.get_rect()

        ballRect.top = HEIGHT//2 - ballRect.height//2

        ballRect.left = WIDTH//2 - ballRect.width//2

        road = 1
        road = ma.Roads(ballRect, road)


        flag = 1

        pygame.display.set_caption("ZigZag")

        ballSpeed = [speedFactor,0]
        while True:

            """
            Обработка нажатий
            """

            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        score += 1
                        ballSpeed[0] = -ballSpeed[0]

                    elif event.key == pygame.K_LEFT:
                        if ballSpeed[0] > 0:
                            score += 1
                            ballSpeed[0] = -ballSpeed[0]

                    elif event.key == pygame.K_RIGHT:
                        if ballSpeed[0] < 0:
                            score += 1
                            ballSpeed[0] = -ballSpeed[0]

            """
            Проверка на окончание игры
            """
            if ma.gameOver(ballRect, 3*ballRect.width):

                while True:
                    background.fill(BACKGROUND)
                    label = font40.render("Игра окончена. Твой счет: %d" % (score), 1, TEXT)
                    labelrect = label.get_rect()
                    labelrect.centerx = background.get_rect().centerx
                    labelrect.centery = background.get_rect().centery

                    highScore = max(score, highScore)
                    highScoreLabel = font40.render("Лучший счет: %d" % (highScore), 1, TEXT)
                    highScoreLabelRect = highScoreLabel.get_rect()
                    highScoreLabelRect.centerx = background.get_rect().centerx
                    highScoreLabelRect.centery = background.get_rect().centery + 2*labelrect.height

                    againLabel = font40.render("Нажми ENTER чтобы начать заново", 1, TEXT)
                    againLabelRect = againLabel.get_rect()
                    againLabelRect.centerx = background.get_rect().centerx
                    againLabelRect.centery = background.get_rect().centery + 4*labelrect.height

                    background.blit(label,labelrect)
                    background.blit(highScoreLabel,highScoreLabelRect)
                    background.blit(againLabel,againLabelRect)

                    screen.blit(background, (0,0))
                    pygame.display.flip()
                    if ma.waitForKeyPress() == pygame.K_RETURN:
                        return
                    else:
                        continue


            ballRect = ballRect.move(ballSpeed[0], ballSpeed[1])

            """
            Добавление дороги, когда вторая последняя точка находится на экране, а последняя точка находится вне экрана
            """
            if roadPoints[-1][1]+HEIGHT <= 0 and roadPoints[-2][1]+HEIGHT >= 0:
                roadPoints.append(ma.addRoad(roadPoints[-1][0], roadPoints[-1][1], road))
                road = 1 - road

            """
            Удалить точки из RoadPoints, когда они больше не нужны
            """
            if roadPoints[1][1] > HEIGHT:
                del roadPoints[0]

            roadPointsLen = len(roadPoints)


            background.fill(BACKGROUND)

            i = roadPointsLen - 1
            roadWidth = 3*ballRect.width

            while i > 0:
                frontPoints = [[roadPoints[i-1][0] + roadWidth//2, roadPoints[i-1][1]], [roadPoints[i-1][0] + roadWidth//2, roadPoints[i-1][1] + int(1.5*roadWidth)], [roadPoints[i-1][0] - roadWidth//2, roadPoints[i-1][1] + int(1.5*roadWidth)], [roadPoints[i-1][0] - roadWidth//2, roadPoints[i-1][1]]]
                if roadPoints[i-1][0] < roadPoints[i][0]:
                    topPoints = [[roadPoints[i-1][0] + roadWidth//2, roadPoints[i-1][1]], [roadPoints[i][0] + roadWidth//2, roadPoints[i][1]], [roadPoints[i][0] - roadWidth//2, roadPoints[i][1]], [roadPoints[i-1][0] - roadWidth//2, roadPoints[i-1][1]]]
                    rectPoints = [[roadPoints[i - 1][0] + roadWidth // 2, roadPoints[i - 1][1]],
                                  [roadPoints[i][0] + roadWidth // 2, roadPoints[i][1]],
                                  [roadPoints[i][0] + roadWidth // 2, roadPoints[i][1] + int(1.5 * roadWidth)],
                                  [roadPoints[i - 1][0] + roadWidth // 2, roadPoints[i - 1][1] + int(1.5 * roadWidth)]]
                    pygame.draw.polygon(background, RIGHTROAD, rectPoints, 0)

                else:
                    topPoints = [[roadPoints[i-1][0] + roadWidth//2, roadPoints[i-1][1]], [roadPoints[i][0] + roadWidth//2, roadPoints[i][1]], [roadPoints[i][0] - roadWidth//2, roadPoints[i][1]], [roadPoints[i-1][0] - roadWidth//2, roadPoints[i-1][1]]]
                    rectPoints = [[roadPoints[i - 1][0] - roadWidth // 2, roadPoints[i - 1][1]],
                                  [roadPoints[i][0] - roadWidth // 2, roadPoints[i][1]],
                                  [roadPoints[i][0] - roadWidth // 2, roadPoints[i][1] + int(1.5 * roadWidth)],
                                  [roadPoints[i - 1][0] - roadWidth // 2, roadPoints[i - 1][1] + int(1.5 * roadWidth)]]
                    pygame.draw.polygon(background, LEFTROAD, rectPoints, 0)

                pygame.draw.polygon(background, LEFTROAD, frontPoints, 0)
                pygame.draw.polygon(background, ROAD, topPoints, 0)
                i -= 1

            for i in range(roadPointsLen):
                roadPoints[i][1] += 1

            background.blit(ball, ballRect)

            if flag:


                label = font40.render("Нажми на ПРОБЕЛ чтобы начать игру", 1, TEXT)
                labelrect = label.get_rect()
                labelrect.centerx = background.get_rect().centerx
                labelrect.centery = HEIGHT - 6*labelrect.height
                againLabel = font15.render("Используй стрелочки/пробел, чтобы изменять направление шарика", 1, TEXT)
                againLabelRect = againLabel.get_rect()
                againLabelRect.centerx = background.get_rect().centerx
                againLabelRect.centery = HEIGHT - 4*labelrect.height
                background.blit(label, labelrect)
                background.blit(againLabel,againLabelRect)

            scoreText = font40.render("%d" % (score), 1, TEXT)
            scoreTextRect = scoreText.get_rect()
            scoreTextRect.top = scoreTextRect.height
            scoreTextRect.left = WIDTH - scoreTextRect.width - scoreTextRect.height
            background.blit(scoreText, scoreTextRect)
            screen.blit(background, (0,0))
            pygame.display.flip()

            if flag:
                while True:
                    if ma.waitForKeyPress() == pygame.K_SPACE:
                        flag = 0
                        break

            FPSCLOCK.tick(FPS)

ma = Main()

def main():
	global segLen, segFactors, road, roadPoints, speedFactor, highScore, score
	highScore = 0
	segLen = 10
	ma = Main()
	segFactors = [1,1,1,1,1,2,2,2,2,2,3]
	road = 1
	roadPoints = []
	speedFactor = 2
	while True:
		roadPoints = []
		ma.playGame()


if __name__ == '__main__':
	main()
