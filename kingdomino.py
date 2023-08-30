import cv2 as cv

def main():
    print("King Domino points calculator")
    img = cv.imread(r"C:\Users\admin\Downloads\King Domino dataset\1.jpg")
    cv.imshow("Game board", img)
    cv.waitKey(0)

if __name__ == "__main__":
    main()