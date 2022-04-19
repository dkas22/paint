import sys
from help_window import MainWindow1

from PyQt5.QtWidgets import QAction, QApplication, QColorDialog, QFileDialog,  QLabel, QMainWindow,  QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSlider, QStatusBar, QToolBar, QToolButton, QWidget, qApp;
from PyQt5.QtGui import QColor,  QFont,  QIcon, QImage, QPainter, QBrush, QPainterPath, QPalette, QPen, QPixmap, QPolygon, QResizeEvent
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter;
import random
import math
from design import Ui_MainWindow;

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("./img/icon.png"))
        self.setGeometry(100,100,1282,725+127);
        self.setMinimumWidth(1000);
        self.setMinimumHeight(600);
        
        self.scale = 1;
    
        self.ui.body.setContentsMargins(0,0,0,0)
        self.ui.toolbarArea.setContentsMargins(0,0,0,0)
        self.ui.body.setContentsMargins(0,0,0,0)
        self.ui.paintArea.setContentsMargins(0,0,0,0)
        self.ui.statusbar.setFixedHeight(30)
        self.ui.toolbarArea.setFixedHeight(80)
        self.ui.toolbarArea.setMinimumWidth(1000);
        self.ui.color.setFixedWidth(60);
        self.ui.editColor.setFixedWidth(60)
        self.ui.editColor.setFixedHeight(60);
        self.ui.editColor.setIcon(QIcon("./img/editcolor.png"));
        self.ui.editColor.setIconSize(QSize(55,55));
        self.ui.toolbarArea.setStyleSheet("background-color:#a4b787")


        self.ui.statusbar.setStyleSheet("background-color:#adce74")

        


        
        


        self.ui.menubar.setStyleSheet("background-color:#adce74")
        self.ui.centralwidget.setStyleSheet("background-color:#8fd6e1")
        self.ui.selectFontSize.setFont(QFont('Arial',10))
        self.ui.brushSize.setFont(QFont('Arial',10))
        self.ui.lineWidth.setFont(QFont('Arial',10))
        self.ui.selectFont.setFont(QFont('Arial',10))
        self.ui.paintArea.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.ui.paintArea.setStyleSheet("background-color:yellow");
        self.ui.selectFontSize.setMinimumWidth(60);
        self.ui.selectFont.setFixedHeight(25);
        self.ui.selectFontSize.setFixedHeight(25);
        
        self.ui.lineWidth.setMinimumWidth(60);
        self.ui.lineWidth.setFixedHeight(25);
        self.ui.brushSize.setMinimumWidth(60)
        self.ui.brushSize.setFixedHeight(25)
        self.ui.selectFontSize.addItem('Font Size')
        self.ui.selectFontSize.addItems([str(i) for i in range(8,73) if i%2==0])
        self.ui.selectFontSize.setCurrentText('12')
        self.fontList = ['Arial','Times New Roman','Helvetica','Times','Courier New','Verdana',
        'Courier','Arial Narrow','Candara','Geneva','Calibri','Optima','Cambria',
        'Garamond','Perpetua','Monaco','Didot','Brush Script MT','Lucida Bright','Copperplate'];

        self.ui.selectFont.addItem('Select Font');
        self.ui.selectFont.setCurrentText('Arial')
        
        self.ui.selectFont.addItems(sorted(self.fontList));
        self.ui.selectFont.setCurrentText('Arial')
        self.ui.selectFontSize.setCurrentText('12');

        self.ui.brushSize.addItems(['Brush Size','2px','3px','4px','5px','6px','8px','10px','12px','14px','16px','18px','20px','22px','24px','26px','28px','30px','32px','34px','36px'])
        self.ui.brushSize.setCurrentText('3px');
        self.ui.lineWidth.addItems(['Line Width','2px','3px','4px','5px','6px','8px','10px','12px','14px','16px','18px','20px','22px','24px','26px','28px','30px','32px','34px','36px'])
        self.ui.lineWidth.setCurrentText('2px');
        
        self.title = "Paint";
        self.currentTool = 'pen';
        self.currentColor = Qt.black;
        self.surfaceColor = Qt.white;
        self.brushSize = int(self.ui.brushSize.currentText()[:-2]);
        self.lineWidth = int(self.ui.lineWidth.currentText()[:-2]);
        self.fontSize = int(self.ui.selectFontSize.currentText());
        self.fontFamily = self.ui.selectFont.currentText();
        self.isSelectMoveIsActive = False;
        self.isSelectToolWasActive = False;
        self.rubberSize = 6
        self.validClick = False;
        self.fileChanged = False;
        self.savedFilePath = "";

        self.colorImage = QImage(QSize(100,100), QImage.Format_RGB32);
        self.paintSurface = QImage(QSize(1280,720), QImage.Format_RGB32);
        self.paintSurface.fill(self.surfaceColor);
        self.begin = QPoint();
        self.end = QPoint();
        self.selectBegin,self.selectEnd = QPoint(),QPoint();
        self.moveStart ,self.moveEnd = QPoint(),QPoint();
    

        self.items = [QPixmap.fromImage(self.paintSurface)];
        self.items2 = [];

        self.text = "";
        self.drawTextStatus = False;
        self.fontBold = False
        self.fontUnderline = False;
        self.fontItalic = False;
        self.blinkCount = 0;
        self.textStartPos = QPoint();





        # status bar things goes here 
        self.s1 = QSlider(Qt.Horizontal,self.ui.statusbar)
        self.s1.setStyleSheet("""QSlider::groove:horizontal {
                                    border: 1px solid;
                                    border-radius:1px;
                                    height: 3px;
                                    margin: 0px;
                                    background-color:white;
                                    }
                                QSlider::handle:horizontal {
                                    background-color:#29bbff;
                                    border: 1px solid #29bbff;
                                    width: 5px;
                                    margin: -10px 0px;
                                    border-radius:2px;
                                    }""")
        self.s1.setFixedWidth(150)
        self.s1.move(self.width()-190,0);
        self.s1.setTickInterval(10)
        self.s1.setSingleStep(10)
        self.s1.setMinimum(50)
        self.s1.setMaximum(200)
        self.s1.setValue(100)

        self.b1=QPushButton("+",self.ui.statusbar)
        self.b1.setFixedWidth(15)
        self.b1.setFixedHeight(15)
        self.b1.move(self.width()-30,8)

        self.b2=QPushButton("-",self.ui.statusbar)
        self.b2.setFixedWidth(15)
        self.b2.setFixedHeight(15)
        



        self.scaleText = QLabel(self.ui.statusbar);
        self.scaleText.setText("{}%".format(self.scale*100));
        self.scaleText.setFixedWidth(40);
        self.scaleText.move(QPoint(self.width()-255,0))
        self.scaleText.setStyleSheet("font-size:12px;")
        self.ui.paintArea.setPixmap(QPixmap.fromImage(self.paintSurface));

        

        self.setWindowTitle(self.title)
        self.createIcons();
        self.colorSelectFunc();
        self.sketchToolSelectFunc();
        self.assignActionsFunctions();

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.ui.paintArea)
        self.ui.gridLayout.addWidget(self.scrollArea);
        self.scrollArea.setVisible(True)
        
        self.currentToolButton = self.ui.pen;
        self.currentToolButton.setStyleSheet("background:white")

        self.plusRubberAction = QAction(self);
        self.plusRubberAction.setShortcut("Ctrl++")
        self.minusRubberAction =QAction(self);
        self.minusRubberAction.setShortcut("Ctrl+-")


        
    
    def resizeEvent(self, e: QResizeEvent):
        self.b2.move(self.width()-215,8)
        self.b1.move(self.width()-30,8)
        self.s1.move(self.width()-190,0);
        self.scaleText.move(QPoint(self.width()-255,0))
        super().resizeEvent(e)
    
    def assignActionsFunctions(self):
        self.ui.actionNew.triggered.connect(self.clearFunc);
        self.ui.actionOpen.triggered.connect(self.openFunc);
        self.ui.actionSave.triggered.connect(self.saveFunc);
        self.ui.actionSaveAs.triggered.connect(self.saveAsFunc);
        self.ui.actionExit.triggered.connect(self.quitFunc);
        self.ui.actionPrint.triggered.connect(self.printFunc);
        self.ui.actionCut.triggered.connect(self.cutFunc);
        self.ui.actionCopy.triggered.connect(self.copyFunc);
        self.ui.actionCrop.triggered.connect(self.cropFunc);
        self.ui.actionUndo.triggered.connect(self.undoFunc);
        self.ui.actionRedu.triggered.connect(self.redoFunc);
        self.ui.actionZoomIn.triggered.connect(self.zoomInFunc);
        self.ui.actionZoomOut.triggered.connect(self.zoomOutFunc);
        self.ui.actionOriginal.triggered.connect(self.zoomOriginal);
        self.ui.actionToolBar.triggered.connect(self.hideShowToolbar);
        self.ui.actionAbout.triggered.connect(self.show_popup)

        self.b1.clicked.connect(self.zoomInFunc);
        self.b2.clicked.connect(self.zoomOutFunc);

        self.s1.valueChanged[int].connect(self.handleSlider);
    def handleSlider(self,x):
        self.scale = x/100;
        self.updateZoom();
    
    def show_popup(self):
        self.help=MainWindow1()
        self.help.initUI()
        self.help.show()

    def hideShowToolbar(self,value):
        w = self.width();
        h = self.height();
        if not value:
            self.ui.toolbarArea.setHidden(True);
            # self.setGeometry(100,100,w,h-80);
        else:
            self.ui.toolbarArea.setHidden(False);
            # self.setGeometry(100,100,w,h+80)

    def keyPressEvent(self,event):
        if self.currentTool == 'text' and self.drawTextStatus:
            if event.key() == Qt.Key_Backspace:
                self.text = self.text[:-1];
            else:
                self.text +=event.text();
        if event.key() == Qt.Key_Plus and self.currentTool=='eraser':
            self.plusRubberSizeFunc();
        elif event.key() == Qt.Key_Minus and self.currentTool == 'eraser':
            self.minusRubberSizeFunc();
    
    def minusRubberSizeFunc(self):
        print(self.rubberSize)
        if self.rubberSize <=2:
            self.rubberSize = 2;
        else:
            self.rubberSize -=2;
    
    def plusRubberSizeFunc(self):
        print(self.rubberSize);
        if self.rubberSize >= 30:
            self.rubberSize = 30;
        else:
            self.rubberSize +=2;
    
    def checkValidClick(self,e):
        x0,y0 = self.getCorrectPoint(e).x(),self.getCorrectPoint(e).y();
        w,h = self.ui.paintArea.width(),self.ui.paintArea.height();

        if 0<=x0<w and 0<=y0<h:
            return True;
        return False;

    def mousePressEvent(self,event):
        if not self.checkValidClick(event):
            self.validClick = False;
            return;
        self.validClick = True;

        if self.isSelectToolWasActive:
            x,y = self.getCorrectPoint(event).x(), self.getCorrectPoint(event).y();
            x1,y1 = self.selectBegin.x(),self.selectBegin.y()
            x2,y2 = self.selectEnd.x(),self.selectEnd.y()

            x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
            y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

            if x1<x<x2 and y1<y<y2 and self.currentTool=='select':
                self.isSelectMoveIsActive = True;
                self.moveStart = self.getCorrectPoint(event);
                self.moveEnd = self.moveStart;
            else:
                self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
                self.isSelectToolWasActive = False;
                self.isSelectMoveIsActive = False;
                self.selectBegin,self.selectEnd = QPoint(), QPoint();
        if not self.isSelectMoveIsActive:
            if event.button() == Qt.LeftButton and self.currentTool == 'colorPicker':
                self.currentColor = self.paintSurface.pixelColor(self.getCorrectPoint(event))
                self.colorImage.fill(self.currentColor);
                self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
            if event.button() == Qt.LeftButton and self.currentTool == 'text':
                if self.drawTextStatus:
                    if self.text != "":
                        canvasPainter = QPainter(self.paintSurface);
                        x0,y0 = self.textStartPos.x(),self.textStartPos.y();
                        canvasPainter.setPen(QPen(Qt.black, 2, Qt.DashLine))
                        font = self.getFont();
                        canvasPainter.setFont(font);
                        canvasPainter.setPen(self.currentColor)
                        canvasPainter.drawText(x0,y0+self.fontSize, self.text); 
                    self.drawTextStatus = False;
                    self.text = "";
                    self.textStartPos = QPoint();
                else:
                    self.drawTextStatus = True;
                    self.textStartPos = self.getCorrectPoint(event);
                
            elif event.button() == Qt.LeftButton and self.currentTool == 'floodfill':
                x0,y0 = self.getCorrectPoint(event).x(), self.getCorrectPoint(event).y();
                target_color = self.paintSurface.pixel(x0,y0);
                self.floodFillFunc(x0,y0,target_color);
                self.update();
            elif event.button() == Qt.LeftButton and self.currentTool in ['pen','brush']:
                self.begin = self.getCorrectPoint(event);
                self.end = self.getCorrectPoint(event);
                self.update()
            
            elif event.button() == Qt.LeftButton and self.currentTool in ['line','circle','rectangle','ellipse','star','polygon','arrow_right','arrow_left']:
                self.begin = self.getCorrectPoint(event);
                self.end = self.begin;
                self.update();
            elif event.button() == Qt.LeftButton and self.currentTool == 'select':
                self.begin = self.getCorrectPoint(event);
                self.end = self.begin;

                self.selectBegin = self.getCorrectPoint(event);
                self.selectEnd = self.selectBegin;
                self.update();
            elif event.button() == Qt.LeftButton and self.currentTool in ['eraser']:
                self.end = self.getCorrectPoint(event);
                self.update();
            
            elif event.button() == Qt.LeftButton and self.currentTool in ['sprayer']:
                self.radius=2*self.brushSize;
                area = int(math.pi * (self.radius**2))
                n = area//4;
                x0,y0 = self.getCorrectPoint(event).x(),self.getCorrectPoint(event).y();
                painter = QPainter(self.paintSurface);
                painter.setPen(QPen(self.currentColor, 1, Qt.SolidLine))
                painter.setBrush(QBrush(self.currentColor, Qt.SolidPattern))
                for i in range(int(n*0.10)):
                    r = random.randint(0,int(0.2*self.radius))
                    theta = random.randint(0,360);
                    theta = math.radians(theta);
                    x = r*math.cos(theta)
                    y = r*math.sin(theta);
                    x,y = int(x), int(y);
                    painter.drawPoint(QPoint(x0+x,y0+y))
                    self.update();
                for i in range(int(n*0.90)):
                    r = random.randint(int(0.2*self.radius),self.radius)
                    theta = random.randint(0,360);
                    theta = math.radians(theta);
                    x = r*math.cos(theta)
                    y = r*math.sin(theta);
                    x,y = int(x), int(y);
                    painter.drawPoint(QPoint(x0+x,y0+y))
                    self.update();

    def mouseMoveEvent(self,event):
        if not self.validClick:
            return;
        if event.buttons() and Qt.LeftButton and self.isSelectMoveIsActive:
            self.moveEnd = self.getCorrectPoint(event);
            self.update();
        
        elif event.buttons() and Qt.LeftButton and self.currentTool in ['pen','brush']:
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor, 1, Qt.SolidLine));
            if self.currentTool == 'brush':
                painter.setPen(QPen(self.currentColor, self.brushSize, Qt.SolidLine,Qt.RoundCap,Qt.MiterJoin));
            painter.drawLine(self.begin, self.end);
            self.begin = self.end;
            self.end = self.getCorrectPoint(event);
            self.update();
        elif event.buttons() and Qt.LeftButton and self.currentTool == 'eraser':
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.surfaceColor, 2, Qt.SolidLine));
            painter.setBrush(QBrush(self.surfaceColor, Qt.SolidPattern))
            r = self.rubberSize #rubber size
            begin = QPoint(self.end.x()-r,self.end.y()-r);
            end = QPoint(self.end.x()+r,self.end.y()+r);
            rect = QRect(begin, end);
            painter.drawEllipse(rect);
            self.end = self.getCorrectPoint(event);
            self.update();
        elif event.buttons() and Qt.LeftButton and  self.currentTool == 'sprayer':
            self.radius=2*self.brushSize;
            area = int(math.pi * (self.radius**2))
            n = area//10;
            x0,y0 = self.getCorrectPoint(event).x(),self.getCorrectPoint(event).y();
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor, 1, Qt.SolidLine));
            painter.setBrush(QBrush(self.currentColor, Qt.SolidPattern))
            for i in range(int(n*0.10)):
                r = random.randint(0,4)
                theta = random.randint(0,360);
                theta = math.radians(theta);
                x = r*math.cos(theta)
                y = r*math.sin(theta);
                x,y = int(x), int(y);
                painter.drawPoint(QPoint(x0+x,y0+y))
                self.update();
            for i in range(int(n*0.90)):
                r = random.randint(5,self.radius)
                theta = random.randint(0,360);
                theta = math.radians(theta);
                x = r*math.cos(theta)
                y = r*math.sin(theta);
                x,y = int(x), int(y);
                painter.drawPoint(QPoint(x0+x,y0+y))
                self.update();
        elif event.buttons() and Qt.LeftButton and self.currentTool=='select':
            self.end = self.getCorrectPoint(event);
            self.selectEnd = self.getCorrectPoint(event);
            self.update();
        elif event.buttons() and Qt.LeftButton and self.currentTool in ['line','circle','rectangle','ellipse','star','polygon'
        ,'arrow_left','arrow_right']:
            self.end = self.getCorrectPoint(event);
            self.update();
    def generateArrowRight(self):
        x1,y1 = self.begin.x(),self.begin.y()
        x2,y2 = self.end.x(),self.end.y()

        x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
        y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

        w = x2-x1;
        h = y2-y1;

        first = QPoint(x1,y1+h//4);
        second = QPoint(x1+w//2,y1+h//4);
        third = QPoint(x1+w//2,y1);
        forth = QPoint(x1+w,y1+h//2);
        fifth = QPoint(x1+w//2,y1+h);
        sixth = QPoint(x1+w//2,y1+(h//4)*3);
        seventh = QPoint(x1,y1+(h//4)*3);

        arrowRight= QPolygon([
            first,second,third,forth,fifth,sixth,seventh
        ])

        return arrowRight;  
        
    def generateArrowLeft(self):
        x1,y1 = self.begin.x(),self.begin.y()
        x2,y2 = self.end.x(),self.end.y()

        x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
        y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

        w = x2-x1;
        h = y2-y1;

        first = QPoint(x1,y1+h//2);
        second = QPoint(x1+w//2,y1);
        third = QPoint(x1+w//2,y1+h//4);
        forth = QPoint(x1+w,y1+h//4);
        fifth = QPoint(x1+w,y1+(h//4)*3);
        sixth = QPoint(x1+w//2,y1+(h//4)*3);
        seventh = QPoint(x1+w//2,y1+h);

        arrowLeft= QPolygon([
            first,second,third,forth,fifth,sixth,seventh
        ])

        return arrowLeft;  
    
    def generateStar(self):
        x1,y1 = self.begin.x(),self.begin.y()
        x2,y2 = self.end.x(),self.end.y()

        x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
        y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

        w = x2-x1;
        h = y2-y1;
        
        first = QPoint(x1,y1+h//4);
        second = QPoint(x1+w//3,y1+h//4);
        third = QPoint(x1+w//2,y1);
        forth = QPoint(x1+(w//3)*2,y1+h//4);
        fifth = QPoint(x1+w,y1+h//4);
        sixth = QPoint(x1+(w//6)*5,y1+h//2);
        seventh = QPoint(x1+w,y1+(h//4)*3);
        eighth = QPoint(x1+(w//3)*2,y1+(h//4)*3);
        ninth = QPoint(x1+w//2,y1+h);
        tenth = QPoint(x1+w//3,y1+(h//4)*3);
        eleventh = QPoint(x1,y1+(h//4)*3);
        twelth = QPoint(x1+w//6,y1+h//2);
        star = QPolygon([
            first,second,third,forth,fifth,sixth,seventh,eighth,ninth,tenth,eleventh,twelth
        ])

        return star;        
    
    def generatePentagon(self):
        x1,y1 = self.begin.x(),self.begin.y()
        x2,y2 = self.end.x(),self.end.y()

        x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
        y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

        w = x2-x1;
        h = y2-y1;
        
        first = QPoint(x1,y1+(h//8)*3);
        second = QPoint(x1+w//2,y1);
        third = QPoint(x1+w,y1+(h//8)*3);
        forth = QPoint(x1+(w//5)*4,y1+h);
        fifth = QPoint(x1+(w//5),y1+h);

        pentagon = QPolygon([first,second,third,forth,fifth]);
        return pentagon;
    
    def mouseReleaseEvent(self,event):
        if not self.validClick:
            return;
        if event.button() == Qt.LeftButton and self.currentTool in ['pen','brush']:
            self.end = QPoint();
            self.update();

        elif event.button() == Qt.LeftButton and self.currentTool=='eraser':
            self.end = QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='rectangle': # button not buttons
            rect = QRect(self.begin, self.end);
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor,self.lineWidth, Qt.SolidLine));
            painter.drawRect(rect);
    
            self.begin,self.end = QPoint(), QPoint();
            self.update();

        elif event.button() == Qt.LeftButton and self.currentTool=='star': # button not buttons
            
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor,self.lineWidth, Qt.SolidLine));
            
            star = self.generateStar();
            painter.drawPolygon(star);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='arrow_right': # button not buttons
            
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor,self.lineWidth, Qt.SolidLine));
            
            arrow_right = self.generateArrowRight();
            painter.drawPolygon(arrow_right);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='arrow_left': # button not buttons
            
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor,self.lineWidth, Qt.SolidLine));
            
            arrow_left= self.generateArrowLeft();
            painter.drawPolygon(arrow_left);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='polygon': # button not buttons
            
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor,self.lineWidth, Qt.SolidLine));
            
            pentagon = self.generatePentagon();
            painter.drawPolygon(pentagon);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='select': # button not buttons
            if self.isSelectMoveIsActive:
                tempImage = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
                cropedImage = tempImage.copy(QRect(self.selectBegin,self.selectEnd));
                planeImage = tempImage.copy(QRect(self.selectBegin,self.selectEnd));
                # planeImage.fill(self.surfaceColor);
                xdist = self.moveEnd.x() - self.moveStart.x();
                ydist = self.moveEnd.y() - self.moveStart.y();
                x1,y1 = self.selectBegin.x(),self.selectBegin.y()
                x2,y2 = self.selectEnd.x(),self.selectEnd.y()

                x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
                y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

                origin = QPoint(x1+xdist,y1+ydist);
                self.paintSurface = tempImage;
                painter = QPainter(self.paintSurface);
                painter.drawImage(QRect(QPoint(x1,y1),cropedImage.size()),planeImage);
                painter.drawImage(QRect(origin,cropedImage.size()),cropedImage);
                self.isSelectMoveIsActive = False;
                self.isSelectToolWasActive = False;
                self.begin,self.end = QPoint(), QPoint();
                self.moveStart,self.moveEnd = QPoint(), QPoint();
                pixmap = QPixmap().fromImage(self.paintSurface);
                self.items.append(pixmap);
                self.update();
            else:
                self.isSelectToolWasActive = True;
                rect = QRect(self.begin, self.end);
                painter = QPainter(self.paintSurface);
                painter.setPen(QPen(Qt.black, 2, Qt.DashLine));
                painter.drawRect(rect);

                self.begin,self.end = QPoint(), QPoint();
                self.update();
        
        elif event.button() == Qt.LeftButton and self.currentTool=='ellipse': # button not buttons
            rect = QRect(self.begin, self.end);
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor, self.lineWidth, Qt.SolidLine));
            painter.drawEllipse(rect);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='circle': # button not buttons
            r = int(pow((self.begin.x() - self.end.x())**2 + (self.begin.y() - self.end.y())**2 ,0.5))
            begin = QPoint(self.begin.x()-r,self.begin.y()-r);
            end = QPoint(self.begin.x()+r,self.begin.y()+r);
            rect = QRect(begin, end);
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor, self.lineWidth, Qt.SolidLine));
            painter.drawEllipse(rect);
            # painter.drawRect(rect);
            self.begin,self.end = QPoint(), QPoint();
            self.update();
        elif event.button() == Qt.LeftButton and self.currentTool=='line': # button not buttons
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.currentColor, self.lineWidth, Qt.SolidLine));
            painter.drawLine(self.begin, self.end);
            self.begin,self.end = QPoint(), QPoint();
            self.update();

        if self.currentTool != 'select':
            pixmap = QPixmap().fromImage(self.paintSurface);
            self.items.append(pixmap);
        self.fileChanged = True;
    

    def getFont(self):
        font = QFont(self.fontFamily);
        font.setPixelSize(self.fontSize);
        font.setBold(self.fontBold);
        font.setUnderline(self.fontUnderline);
        font.setItalic(self.fontItalic);
        return font;

    def paintEvent(self, event):
        maskSurface = QImage(self.paintSurface.size(), QImage.Format_RGB32);
        maskSurface.fill(self.surfaceColor);
        canvasPainter = QPainter(maskSurface);
        canvasPainter.drawImage(self.paintSurface.rect(),self.paintSurface);
        
        canvasPainter.setPen(QPen(self.currentColor, self.brushSize, Qt.SolidLine));
        if self.isSelectMoveIsActive and not self.moveStart.isNull() and not self.moveEnd.isNull():
            tempImage = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            cropedImage = tempImage.copy(QRect(self.selectBegin,self.selectEnd));

            planeImage = tempImage.copy(QRect(self.selectBegin,self.selectEnd));
            # planeImage.fill(self.surfaceColor);
            xdist = self.moveEnd.x() - self.moveStart.x();
            ydist = self.moveEnd.y() - self.moveStart.y();
            x1,y1 = self.selectBegin.x(),self.selectBegin.y()
            x2,y2 = self.selectEnd.x(),self.selectEnd.y()

            x1,x2 = (x1,x2) if x1<=x2 else (x2,x1);
            y1,y2 = (y1,y2) if y1<=y2 else (y2,y1);

            origin = QPoint(x1+xdist,y1+ydist);
            canvasPainter.drawImage(QRect(QPoint(x1,y1),cropedImage.size()),planeImage);
            canvasPainter.drawImage(QRect(origin,cropedImage.size()),cropedImage);
            canvasPainter.setPen(QPen(Qt.black,2,Qt.DashLine));
            rect = QRect(origin,cropedImage.size());
            canvasPainter.setPen(QPen(self.currentColor,2,Qt.DashLine));
            canvasPainter.drawRect(rect);

        if self.currentTool == 'text' and self.drawTextStatus:
            x0,y0 = self.textStartPos.x(),self.textStartPos.y();
            canvasPainter.setPen(QPen(Qt.black, 2, Qt.DashLine))
            font = self.getFont();
            canvasPainter.setFont(font);
            canvasPainter.setPen(self.currentColor)
            temp = "";
            if (self.blinkCount//25)%2==0:
                temp = self.text+ "_";
                if self.blinkCount > 50000:
                    self.blinkCount = 0;
            else:
                temp = self.text;
            self.blinkCount +=1;
            canvasPainter.drawText(x0,y0+self.fontSize, temp); 
        elif not self.end.isNull() and self.currentTool=='eraser':
            canvasPainter.setPen(QPen(Qt.black, 2, Qt.SolidLine));
            r = self.rubberSize #rubber size
            begin = QPoint(self.end.x()-r,self.end.y()-r);
            end = QPoint(self.end.x()+r,self.end.y()+r);
            rect = QRect(begin, end);
            canvasPainter.drawEllipse(rect);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='rectangle':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            rect = QRect(self.begin, self.end);
            canvasPainter.drawRect(rect);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='star':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            star = self.generateStar();
            canvasPainter.drawPolygon(star);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='arrow_right':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            arrowRight = self.generateArrowRight();
            canvasPainter.drawPolygon(arrowRight);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='arrow_left':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            arrowLeft = self.generateArrowLeft();
            canvasPainter.drawPolygon(arrowLeft);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='polygon':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            pentagon = self.generatePentagon();
            canvasPainter.drawPolygon(pentagon);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='select':
            canvasPainter.setPen(QPen(Qt.black,2,Qt.DashLine));
            rect = QRect(self.begin, self.end);
            canvasPainter.drawRect(rect); 
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='ellipse':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            rect = QRect(self.begin, self.end);
            canvasPainter.drawEllipse(rect);

        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='circle':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            r = int(pow((self.begin.x() - self.end.x())**2 + (self.begin.y() - self.end.y())**2 ,0.5))
            begin = QPoint(self.begin.x()-r,self.begin.y()-r);
            end = QPoint(self.begin.x()+r,self.begin.y()+r);
            rect = QRect(begin, end);
            canvasPainter.drawEllipse(rect);
        elif not self.begin.isNull() and not self.end.isNull() and self.currentTool=='line':
            canvasPainter.setPen(QPen(self.currentColor,self.lineWidth,Qt.SolidLine))
            canvasPainter.drawLine(self.begin, self.end);
        canvasPainter.end();

        image = maskSurface.scaled(int(maskSurface.width()*self.scale), int(maskSurface.height()*self.scale), Qt.KeepAspectRatio)
        self.ui.paintArea.setPixmap(QPixmap().fromImage(image));
        self.ui.paintArea.adjustSize();
    def getCorrectPoint(self,event):
        h=self.scrollArea.horizontalScrollBar().value();
        v=self.scrollArea.verticalScrollBar().value();

        if self.ui.actionToolBar.isChecked():
            y = event.y()-100+v;
        else:
            y = event.y()-20+v;
        x = event.x()+h;

        x = int(x/self.scale);
        y = int(y/self.scale);
        return QPoint(x,y);
    def createIcons(self):
        self.ui.blue.setIcon(QIcon("img/blue.png"))
        self.ui.orange.setIcon(QIcon('./img/orange.png'))
        self.ui.green.setIcon(QIcon('./img/green.png'))
        self.ui.yellow.setIcon(QIcon('./img/yellow.png'))
        self.ui.red.setIcon(QIcon('./img/red.png'))
        self.ui.black.setIcon(QIcon('./img/black.png'))
        self.ui.white.setIcon(QIcon('./img/white.png'))
        self.ui.indigo.setIcon(QIcon('./img/indigo.png'))
        self.ui.gray.setIcon(QIcon('./img/gray.png'))
        self.ui.brown.setIcon(QIcon('./img/brown.png'))
        self.ui.pink.setIcon(QIcon('./img/pink.png'))
        self.ui.violet.setIcon(QIcon('./img/violet.png'))
        self.ui.selectFontBold.setIcon(QIcon('./img/bold_text.png'))
        self.ui.selectFontItalic.setIcon(QIcon('./img/italic_text.png'))
        self.ui.selectFontUnderline.setIcon(QIcon('./img/underline_text.png'))

        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));



        self.ui.pen.setIcon(QIcon("./img/pencil2.png"));
        self.ui.brush.setIcon(QIcon("./img/paintbrush.png"));
        self.ui.floodFill.setIcon(QIcon("./img/floodfill.png"));
        self.ui.select.setIcon(QIcon("./img/select.png"));
        self.ui.new_2.setIcon(QIcon("./img/newFile.png"));
        self.ui.save.setIcon(QIcon("./img/save.png"));
        self.ui.open.setIcon(QIcon("./img/folder.png"));
        self.ui.insert.setIcon(QIcon("./img/insertPicture.png"));
        self.ui.colorPicker.setIcon(QIcon("./img/color-picker.png"));
        self.ui.text.setIcon(QIcon("./img/text.png"));
        self.ui.eraser.setIcon(QIcon("./img/eraser.png"));
        self.ui.sprayer.setIcon(QIcon("./img/spray.png"));
        self.ui.star.setIcon(QIcon("./img/star.png"));
        self.ui.line.setIcon(QIcon("./img/diagonal-line.png"));
        self.ui.circle.setIcon(QIcon("./img/circle.png"));
        self.ui.ellipse.setIcon(QIcon("./img/ellipse.png"));
        self.ui.rectangle.setIcon(QIcon("./img/rectangle.png"));
        self.ui.rightArrow.setIcon(QIcon("./img/right_arrow.png"));
        self.ui.polygon.setIcon(QIcon("./img/polygon.png"));
        self.ui.leftArrow.setIcon(QIcon("./img/left_arrow.png"));

    def sketchToolSelectFunc(self):
        self.ui.pen.clicked.connect(self.selectPen);
        self.ui.brush.clicked.connect(self.selectBrush);
        self.ui.floodFill.clicked.connect(self.selectFloodFill);
        self.ui.eraser.clicked.connect(self.selectEraser);
        self.ui.sprayer.clicked.connect(self.selectSprayer);
        self.ui.select.clicked.connect(self.selectSelect);
        self.ui.open.clicked.connect(self.openFunc);
        self.ui.save.clicked.connect(self.saveFunc);
        self.ui.new_2.clicked.connect(self.clearFunc);
        self.ui.insert.clicked.connect(self.insertPicture);
        self.ui.line.clicked.connect(self.selectLine);
        self.ui.rectangle.clicked.connect(self.selectRectangle);
        self.ui.circle.clicked.connect(self.selectCircle);
        self.ui.ellipse.clicked.connect(self.selectEllipse);
        self.ui.star.clicked.connect(self.selectStar);
        self.ui.rightArrow.clicked.connect(self.selectArrowRight);
        self.ui.leftArrow.clicked.connect(self.selectArrowLeft);
        self.ui.polygon.clicked.connect(self.selectPolygon);
        self.ui.colorPicker.clicked.connect(self.selectColorPicker);
        self.ui.brushSize.activated[str].connect(self.changeBrushSizeFunc);
        self.ui.selectFontSize.activated[str].connect(self.changeFontSizeFunc);
        self.ui.lineWidth.activated[str].connect(self.changeLineWidthFunc);
        self.ui.selectFont.activated[str].connect(self.changeFontFunc);
        self.ui.text.clicked.connect(self.selectTextTool);
        self.ui.selectFontUnderline.clicked.connect(self.makeUnderlineFunc);
        self.ui.selectFontBold.clicked.connect(self.makeBoldFunc);
        self.ui.selectFontItalic.clicked.connect(self.makeItalicFunc);
    
    def makeUnderlineFunc(self):
        self.fontUnderline = not self.fontUnderline;
        if self.fontUnderline:
            self.ui.selectFontUnderline.setStyleSheet("background:#adce74")
        else:
            self.ui.selectFontUnderline.setStyleSheet("background:#a4b787")
        self.ui.selectFontUnderline.clearFocus();
    def makeBoldFunc(self):
        self.fontBold = not self.fontBold;
        if self.fontBold:
            self.ui.selectFontBold.setStyleSheet("background:#adce74")
        else:
            self.ui.selectFontBold.setStyleSheet("background:#a4b787")
        self.ui.selectFontBold.clearFocus();
    def makeItalicFunc(self):
        self.fontItalic = not self.fontItalic;
        if self.fontItalic:
            self.ui.selectFontItalic.setStyleSheet("background:#adce74")
        else:
            self.ui.selectFontItalic.setStyleSheet("background:#a4b787")
        self.ui.selectFontItalic.clearFocus();
    
    def changeBrushSizeFunc(self,text):
        if text == 'Brush Size':
            self.brushSize = 2;
            return;
        self.brushSize = int(text[:-2]);
        self.ui.brushSize.clearFocus();

    def changeFontSizeFunc(self,text):
        if text == 'Font Size':
            self.fontSize = 12;
            return;
        self.fontSize = int(text);
        self.ui.selectFontSize.clearFocus();

    def changeFontFunc(self,text):
        if text == 'Select Font':
            self.fontFamily = 'Arial';
            return;
        self.fontFamily = text;
        self.ui.selectFont.clearFocus();

    def changeLineWidthFunc(self,text):
        if text == 'Line Width':
            self.lineWidth = 1;
            return;
        self.lineWidth = int(text[:-2]);
        self.ui.lineWidth.clearFocus();
    
    def floodFillFunc(self,x0,y0,targetColor):
        w = self.paintSurface.width();
        h = self.paintSurface.height();

        painter = QPainter(self.paintSurface);
        painter.setPen(QPen(self.currentColor));
        visited = [[False for j in range(0,h)] for i in range(0,w)]
        ques = [(x0,y0)];
        i=0;
        while i<len(ques):
            x,y = ques[i];
            i +=1;
            if visited[x][y]:
                continue;
            visited[x][y] = True;
            if self.paintSurface.pixel(x,y) == targetColor:
                painter.drawPoint(QPoint(x,y));
                if 0<=x+1<w and 0<=y<h and not visited[x+1][y]:
                    ques.append((x+1,y));
                if 0<=x-1<w and 0<=y<h and not visited[x-1][y]:
                    ques.append((x-1,y));
                if 0<=x<w and 0<=y+1<h and not visited[x][y+1]:
                    ques.append((x,y+1));
                if 0<=x<w and 0<=y-1<h and not visited[x][y-1]:
                    ques.append((x,y-1));

    def selectArrowLeft(self):
        self.currentTool = 'arrow_left';
        self.selectCursor();
    def selectArrowRight(self):
        self.currentTool = 'arrow_right';
        self.selectCursor();
    def selectStar(self):
        self.currentTool = 'star';
        self.selectCursor();
    def selectEllipse(self):
        self.currentTool = 'ellipse';
        self.selectCursor();
    def selectCircle(self):
        self.currentTool = 'circle';
        self.selectCursor();
    def selectRectangle(self):
        self.currentTool = 'rectangle';
        self.selectCursor();
    def selectPolygon(self):
        self.currentTool = 'polygon';
        self.selectCursor();
    def selectLine(self):
        self.currentTool = 'line';
        self.selectCursor();
    def selectPen(self):
        self.currentTool = 'pen';
        self.selectCursor();
    def selectColorPicker(self):
        self.currentTool = 'colorPicker';
        self.selectCursor();
    def selectTextTool(self):
        self.currentTool = 'text';
        self.selectCursor();
    
    def selectBrush(self):
        self.currentTool = 'brush';
        self.selectCursor();
    def selectFloodFill(self):
        self.currentTool = 'floodfill';
        self.selectCursor();
    def selectSelect(self):
        self.currentTool = 'select';
        self.selectCursor();
    def selectEraser(self):
        self.currentTool = 'eraser';
        self.selectCursor();
    def selectSprayer(self):
        self.currentTool = 'sprayer';
        self.selectCursor();
        

    def selectCursor(self):
        if self.currentToolButton!="":
            self.currentToolButton.setStyleSheet("background:#a4b787")
        self.currentToolButton = "";
        if self.currentTool == 'pen':
            self.currentToolButton = self.ui.pen;
        if self.currentTool == 'rectangle':
            self.currentToolButton = self.ui.rectangle;
        if self.currentTool == 'circle':
            self.currentToolButton = self.ui.circle;
        if self.currentTool == 'floodfill':
            self.currentToolButton = self.ui.floodFill;
        if self.currentTool == 'ellipse':
            self.currentToolButton = self.ui.ellipse;
        if self.currentTool == 'line':
            self.currentToolButton = self.ui.line;
        if self.currentTool == 'brush':
            self.currentToolButton = self.ui.brush;
        if self.currentTool == 'select':
            self.currentToolButton = self.ui.select;
        if self.currentTool == 'star':
            self.currentToolButton = self.ui.star;
        if self.currentTool == 'arrow_right':
            self.currentToolButton = self.ui.rightArrow;
        if self.currentTool == 'polygon':
            self.currentToolButton = self.ui.polygon;
        if self.currentTool == 'eraser':
            self.currentToolButton = self.ui.eraser;
        if self.currentTool == 'sprayer':
            self.currentToolButton = self.ui.sprayer;
        if self.currentTool == 'colorPicker':
            self.currentToolButton = self.ui.colorPicker;
        if self.currentTool == 'arrow_left':
            self.currentToolButton = self.ui.leftArrow;
        if self.currentTool == 'text':
            self.currentToolButton = self.ui.text;
        if self.currentToolButton !="":
            self.currentToolButton.setStyleSheet("background:white")

    
    def closeEvent(self, event):
        if self.fileChanged:
            quit_msg = "Do you want to save changes to Untitled?"
            qbox = QMessageBox();
            reply = qbox.question(self,'Paint', 
                            quit_msg, QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if reply ==QMessageBox.Discard:
                event.accept();
            elif reply == QMessageBox.Save:
                self.saveFunc();
                event.accept();
            else:
                event.ignore()
    
    def openFunc(self):
        openPath,_ = QFileDialog.getOpenFileName(self,"Open Image","./","Image Files (*.png *.jpg)");
        if openPath != "":
            if self.fileChanged:
                quit_msg = "Do you want to save changes to Untitled?"
                qbox = QMessageBox();
                reply = qbox.question(self,'Paint', 
                                quit_msg, QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

                if reply == QMessageBox.Cancel:
                    return;
                if reply == QMessageBox.Save:
                    savepath,_ = QFileDialog.getSaveFileName(self,"Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;ALL Files(*.*)");
                    if savepath =="":
                        return;
                    self.paintSurface.save(savepath);
            self.fileChanged=False;
            tempImage = QImage(openPath);
            tempImage2 = QImage(tempImage.size(), QImage.Format_RGB32);
            tempImage2.fill(self.surfaceColor);
            painter = QPainter(tempImage2);
            painter.drawImage(tempImage.rect(),tempImage);
            self.paintSurface = tempImage2;
            pixmap = QPixmap.fromImage(self.paintSurface);
            self.setWindowTitle("Paint "+openPath);
            self.items.clear();
            self.items2.clear();
            self.items.append(pixmap);
            self.ui.paintArea.setPixmap(QPixmap.fromImage(self.paintSurface));
            self.ui.paintArea.adjustSize();
            self.update();
    
    def clearFunc(self):
        if self.fileChanged:
            quit_msg = "Do you want to save changes to Untitled?"
            qbox = QMessageBox();

            qbox.setIcon(QMessageBox.NoIcon);
            reply = qbox.question(self,'Paint', 
                            quit_msg, QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return;
            if reply == QMessageBox.Save:
                self.saveFunc();
        self.paintSurface = QImage(QSize(1280,720), QImage.Format_RGB32);
        self.paintSurface.fill(self.surfaceColor);
        self.items = [QPixmap.fromImage(self.paintSurface)]
        self.ui.paintArea.setPixmap(QPixmap.fromImage(self.paintSurface));
        self.ui.paintArea.adjustSize();
        self.items2.clear();
        self.setWindowTitle(self.title);
        self.fileChanged = False;
        self.update();
    
    def insertPicture(self):
        if not self.selectBegin.isNull() and not self.selectEnd.isNull():
            filepath,_ = QFileDialog.getOpenFileName(self,"Open Image","./","Image Files (*.png *.jpg)");
            if filepath !="":
                self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
                painter = QPainter(self.paintSurface);
                tempImage = QImage(filepath);
                painter.drawImage(QRect(self.selectBegin,self.selectEnd),tempImage);
                pixmap = QPixmap().fromImage(self.paintSurface);
                self.items.append(pixmap);
                self.fileChanged = True;
                self.selectBegin,self.selectEnd = QPoint(), QPoint();
                self.update();
        else:
            filepath,_ = QFileDialog.getOpenFileName(self,"Open Image","./","Image Files (*.png *.jpg)");
            if filepath !="":
                painter = QPainter(self.paintSurface);
                tempImage = QImage(filepath);
                painter.drawImage(tempImage.rect(),tempImage);
                pixmap = QPixmap().fromImage(self.paintSurface);
                self.items.append(pixmap);
                self.fileChanged = True;
                self.selectBegin,self.selectEnd = QPoint(), QPoint();
                self.update();
    
    def cutFunc(self):
        if not self.selectBegin.isNull() and not self.selectEnd.isNull():
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            painter = QPainter(self.paintSurface);
            painter.setPen(QPen(self.surfaceColor));
            painter.setBrush(QBrush(self.surfaceColor));
            painter.drawRect(QRect(self.selectBegin,self.selectEnd));
            pixmap = QPixmap().fromImage(self.paintSurface);
            self.items.append(pixmap);
            self.isSelectToolWasActive = False;
            self.isSelectMoveIsActive = False;
            self.selectBegin,self.selectEnd = QPoint(),QPoint();
            self.fileChanged = True;
            self.update();
    
    def copyFunc(self):
        if self.currentTool == 'select' and not self.selectBegin.isNull() and not self.selectEnd.isNull():
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            cropedImage = self.paintSurface.copy(QRect(self.selectBegin,self.selectEnd));
            painter = QPainter(self.paintSurface);
            painter.drawImage(cropedImage.rect(),cropedImage)
            pixmap = QPixmap().fromImage(self.paintSurface);
            self.items.append(pixmap);
            self.isSelectToolWasActive = False;
            self.isSelectMoveIsActive = False;
            self.selectBegin,self.selectEnd = QPoint(),QPoint();
            self.fileChanged = True;
            self.update();
    def cropFunc(self):
        if self.currentTool == 'select' and not self.selectBegin.isNull() and not self.selectEnd.isNull():
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            cropedImage = self.paintSurface.copy(QRect(self.selectBegin,self.selectEnd));

            self.paintSurface = cropedImage;
            pixmap = QPixmap().fromImage(self.paintSurface);
            self.items.append(pixmap);
            self.isSelectToolWasActive = False;
            self.isSelectMoveIsActive = False;
            self.selectBegin,self.selectEnd = QPoint(),QPoint();
            self.fileChanged = True;
            self.update();

    def cropImage(self):
        if not self.selectBegin.isNull() and not self.selectEnd.isNull():
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            self.paintSurface = self.paintSurface.copy(QRect(self.selectBegin,self.selectEnd));

            pixmap = QPixmap().fromImage(self.paintSurface);
            self.items.clear();
            self.items2.clear();
            self.items.append(pixmap);
            self.ui.paintArea.setPixmap(QPixmap.fromImage(self.paintSurface));
            self.ui.paintArea.adjustSize();
            self.fileChanged=True;

    def undoFunc(self):
        if len(self.items) > 1:
            top = self.items[-1];
            self.items.pop();
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            self.items2.insert(0,top);
            self.update();
    
    def redoFunc(self):
        if len(self.items2)>0:
            first = self.items2[0];
            self.items2.pop(0);
            self.items.append(first);
            self.paintSurface = self.items[-1].toImage().convertToFormat(QImage.Format_RGB32);
            self.update();
    
    def saveFunc(self):
        if self.savedFilePath !="":
            self.paintSurface.save(self.savedFilePath);
        else:
            filepath,_ = QFileDialog.getSaveFileName(self,"Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;ALL Files(*.*)");
            if filepath =="":
                return;
            self.setWindowTitle("Paint "+filepath);
            self.paintSurface.save(filepath);
            self.savedFilePath = filepath;
            self.fileChanged = False;
            self.update();
    
    def saveAsFunc(self):
        filepath,_ = QFileDialog.getSaveFileName(self,"Save Paint", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;ALL Files(*.*)");
        if filepath =="":
            return;
        self.setWindowTitle("Paint "+filepath);
        self.paintSurface.save(filepath);
        self.savedFilePath = filepath;
        self.fileChanged = False;
        self.update();
    def printFunc(self):
        # Create printer
        printer =QPrinter(QPrinter.HighResolution)
        x,y = printer.pageRect().width(),printer.pageRect().height();
        # print(x,y);
        # Create painter
        painter = QPainter()
        # Start painter
        painter.begin(printer)
        # Grab a widget you want to print
        screen = self.ui.paintArea.grab()
        # Draw grabbed pixmap
        painter.drawPixmap(0,0, screen)
        # End painting
        painter.end()
    def quitFunc(self):
        qApp.quit();

    def updateZoom(self):
        w = self.paintSurface.width();
        h = self.paintSurface.height();
        self.scaleText.setText("{}%".format(int(self.scale*100)));
        self.s1.setValue(int(self.scale*100));
        image = self.paintSurface.scaled(int(w*self.scale), int(h*self.scale) ,Qt.KeepAspectRatio)
        self.ui.paintArea.setPixmap(QPixmap.fromImage(image));
        self.ui.paintArea.adjustSize();

    def zoomInFunc(self):
        if self.scale >=2:
            self.scale = 2;
            self.scale = round(self.scale,1);
        else:
            self.scale +=0.1;
            self.scale = round(self.scale,1);
        self.updateZoom();
        
    def zoomOutFunc(self):
        if self.scale <= 0.5:
            self.scale = 0.5;
            self.scale = round(self.scale,1);
        else:
            self.scale -=0.1;
            self.scale = round(self.scale,1);
        self.updateZoom();
    def zoomOriginal(self):
        self.scale = 1;
        self.updateZoom();
    
    def colorSelectFunc(self):
        self.ui.violet.clicked.connect(self.selectViolet);
        self.ui.green.clicked.connect(self.selectGreen);
        self.ui.red.clicked.connect(self.selectRed);
        self.ui.blue.clicked.connect(self.selectBlue);
        self.ui.black.clicked.connect(self.selectBlack);
        self.ui.gray.clicked.connect(self.selectGray);
        self.ui.indigo.clicked.connect(self.selectIndigo);
        self.ui.pink.clicked.connect(self.selectPink);
        self.ui.brown.clicked.connect(self.selectBrown);
        self.ui.yellow.clicked.connect(self.selectYellow);
        self.ui.orange.clicked.connect(self.selectOrange);
        self.ui.white.clicked.connect(self.selectWhite);

        self.ui.editColor.clicked.connect(self.editColor);

    def selectViolet(self):
        self.currentColor = QColor(163,73,164);
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.violet.clearFocus();
    def selectRed(self):
        self.currentColor = QColor(255,0,0);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.red.clearFocus();
    def selectBlue(self):
        self.currentColor = QColor(0,0,255);
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.update();
        self.ui.blue.clearFocus();
    def selectGreen(self):
        self.currentColor = QColor(0,255,0);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.green.clearFocus();
    def selectWhite(self):
        self.currentColor = QColor(255,255,255);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.white.clearFocus();
    def selectBlack(self):
        self.currentColor = QColor(0,0,0);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.black.clearFocus();
    def selectYellow(self):
        self.currentColor = QColor(255,255,0);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.yellow.clearFocus();
    def selectPink(self):
        self.currentColor = QColor(255,0,255);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.pink.clearFocus();
    def selectBrown(self):
        self.currentColor = QColor(185,122,87);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.brown.clearFocus();
    def selectGray(self):
        self.currentColor = QColor(195,195,195);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.gray.clearFocus();
    def selectIndigo(self):
        self.currentColor = QColor(63,72,204);
        self.update();
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.indigo.clearFocus();
    def selectOrange(self):
        self.currentColor = QColor(255,127,39);
        self.colorImage.fill(self.currentColor);
        self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.orange.clearFocus();
    def editColor(self):
        color = QColorDialog.getColor();
        if color.isValid():
            self.currentColor = color;
            self.colorImage.fill(self.currentColor);
            self.ui.color.setPixmap(QPixmap().fromImage(self.colorImage));
        self.ui.editColor.clearFocus();

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

