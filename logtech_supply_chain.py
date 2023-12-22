from tkinter import *
from PIL import ImageTk,Image
from time import sleep
import random
import pygame
img=[0,0,0,0]
game=Tk()
game.title("Logtech supply chain ")
canvas=Canvas(master=game,width=900,height=500)
canvas.pack()
bg_img=ImageTk.PhotoImage(Image.open("D:\\plane\\bg.jpg"))
startbutton_img=ImageTk.PhotoImage(Image.open("D:\\plane\\stb.png"))
soundbutton_img=ImageTk.PhotoImage(Image.open("D:\\plane\\sob.png"))
background_img=ImageTk.PhotoImage(Image.open("D:\\plane\\background.jpg"))
order_img=ImageTk.PhotoImage(Image.open("D:\\plane\\order.png"))
background1=canvas.create_image(0, 0, anchor=NW, image=background_img)
background2=canvas.create_image(900, 0, anchor=NW, image=background_img)
img[0]=ImageTk.PhotoImage(Image.open("D:\\plane\\plane.png"))
img[1]=ImageTk.PhotoImage(Image.open("D:\\plane\\cloud.png"))
img[2]=ImageTk.PhotoImage(Image.open("D:\\plane\\sun.png"))
img[3]=ImageTk.PhotoImage(Image.open("D:\\plane\\building.png"))
pygame.init()
game_over_sound=pygame.mixer.Sound("D:\\plane\\gameover.wav")
pygame.mixer.music.load("lxmas.mp3")
pygame.mixer.music.play(-1) 
canvas.update()
def screen_saver():
    bg=canvas.create_image(0,0,anchor=NW,image=bg_img)
    start_button=canvas.create_image(400,150,anchor=NW,image=startbutton_img)
    sound_button=canvas.create_image(400,250,anchor=NW,image=soundbutton_img)
    def start_game(event):
        canvas.delete(ALL)
        game_play()
    def toggle_sound(event):
        if pygame.mixer.music.get_volume()==1:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)
    canvas.tag_bind(start_button, '<Button-1>', start_game)
    canvas.tag_bind(sound_button, '<Button-1>', toggle_sound)
def game_play():
    global cloud, sun, building, order, score, gameover, stopped_background, check_fly, background1, background2
    background1 = canvas.create_image(0, 0, anchor=NW, image=background_img)
    background2 = canvas.create_image(900, 0, anchor=NW, image=background_img)
    plane = canvas.create_image(0, 270, anchor=NW, image=img[0])
    cloud = canvas.create_image(550, 50, anchor=NW, image=img[1])
    sun = canvas.create_image(700, 10, anchor=NW, image=img[2])
    building = canvas.create_image(550, 250, anchor=NW, image=img[3])
    text_score = canvas.create_text(550, 30, text="SCORE:", fill="red", font=("Times", 10))
    gameover = False
    stopped_background = False
    check_fly = False
    order = None
    score = 0
    def moveCloud():
        global cloud
        canvas.move(cloud,-2,0)
        if canvas.coords(cloud)[0]<-70:
            canvas.delete(cloud)
            cloud=canvas.create_image(900,50,anchor=NW,image=img[1])
            canvas.update()
    def moveSun():
        global sun
        canvas.move(sun,-0.5,0)
        if canvas.coords(sun)[0]<-20:
            canvas.delete(sun)
            sun=canvas.create_image(900,10,anchor=NW,image=img[2])
        canvas.update()
    def moveBuilding():
        global building,score
        canvas.move(building,-10,0)
        if canvas.coords(building)[0]<-250:
            canvas.delete(building)
            building=canvas.create_image(1000,250,anchor=NW,image=img[3])
            score+=1
            canvas.itemconfig(text_score,text="SCORE:"+str(score))
        canvas.update()
    def move_background():
        global background1,background2
        canvas.move(background1, -3, 0)
        canvas.move(background2, -3, 0)      
        if canvas.coords(background1)[0] <= -900:
            canvas.move(background1, 1800, 0)         
        if canvas.coords(background2)[0] <= -900:
            canvas.move(background2, 1800, 0)      
        canvas.update()
    game.after(20, move_background)
    def create_order():
        global order
        x=random.randint(0,900)
        y=random.randint(100,150)
        order=canvas.create_image(x,y,anchor=NW,image=order_img)
    create_order()
    def move_order():
        global order,score
        canvas.move(order,-6,0)
        plane_coords = canvas.coords(plane)
        order_coords = canvas.coords(order)
        if (plane_coords[0]<order_coords[0]+50 and plane_coords[0]+80>order_coords[0] and plane_coords[1]<order_coords[1]+50 and plane_coords[1]+80>order_coords[1]):
            score += 1
            canvas.itemconfig(text_score, text="SCORE:" + str(score))
            canvas.delete(order)
            create_order()
        elif order_coords[0]<-100:
            create_order()
    def fly():
        global check_fly
        if check_fly==False:
            check_fly=True
            for i in range(0,40):
                canvas.move(plane,0,-5)
                moveCloud()
                moveBuilding()
                moveSun()
                move_background()
                move_order()
                canvas.update()
                sleep(0.02) 
            for i in range(0,40):
                canvas.move(plane,0,5)
                moveCloud()
                moveBuilding()
                moveSun()
                move_background()
                move_order()
                canvas.update()
                sleep(0.02) 
            check_fly=False
    def keyPress(event):
        if event.keysym=="space":
            fly()
    canvas.bind_all("<KeyPress>",keyPress)
    def check_gameover():
        global gameover,stopped_background
        if canvas.coords(building)[0]<50 and canvas.coords(plane)[1]>220:
            gameover=True
            text_gameover = canvas.create_text(450, 200, text="GAME OVER", fill="red", font=("Times", 60))
            pygame.mixer.music.pause()
            game_over_sound.play()
        if not gameover:
            game.after(100,check_gameover)
    check_gameover()
    while not gameover:
        moveCloud()
        moveSun()
        moveBuilding()
        move_order()
        if not stopped_background:
            move_background()
        sleep(0.02)
screen_saver()
game.mainloop()