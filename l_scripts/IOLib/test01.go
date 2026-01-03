package main

import (
	"fmt"
	"strconv"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	myApp := app.New()
	myWindow := myApp.NewWindow("计算器")

	entry := widget.NewEntry()
	entry.SetPlaceHolder("输入表达式")

	resultLabel := widget.NewLabel("")

	grid := container.NewGridWithColumns(4,
		widget.NewButton("7", func() { entry.SetText(entry.Text + "7") }),
		widget.NewButton("8", func() { entry.SetText(entry.Text + "8") }),
		widget.NewButton("9", func() { entry.SetText(entry.Text + "9") }),
		widget.NewButton("/", func() { entry.SetText(entry.Text + "/") }),

		widget.NewButton("4", func() { entry.SetText(entry.Text + "4") }),
		widget.NewButton("5", func() { entry.SetText(entry.Text + "5") }),
		widget.NewButton("6", func() { entry.SetText(entry.Text + "6") }),
		widget.NewButton("*", func() { entry.SetText(entry.Text + "*") }),

		widget.NewButton("1", func() { entry.SetText(entry.Text + "1") }),
		widget.NewButton("2", func() { entry.SetText(entry.Text + "2") }),
		widget.NewButton("3", func() { entry.SetText(entry.Text + "3") }),
		widget.NewButton("-", func() { entry.SetText(entry.Text + "-") }),

		widget.NewButton("0", func() { entry.SetText(entry.Text + "0") }),
		widget.NewButton(".", func() { entry.SetText(entry.Text + ".") }),
		widget.NewButton("=", func() {
			result, err := strconv.ParseFloat(entry.Text, 64)
			if err == nil {
				resultLabel.SetText(fmt.Sprintf("%f", result))
			} else {
				resultLabel.SetText("错误")
			}
		}),
		widget.NewButton("+", func() { entry.SetText(entry.Text + "+") }),
	)

	content := container.NewVBox(entry, grid, resultLabel)

	myWindow.SetContent(content)
	myWindow.Resize(fyne.NewSize(300, 400))
	myWindow.ShowAndRun()
}
