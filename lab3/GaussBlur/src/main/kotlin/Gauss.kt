package org.example

import com.sksamuel.scrimage.ImmutableImage
import com.sksamuel.scrimage.filter.GrayscaleFilter
import com.sksamuel.scrimage.nio.JpegWriter
import com.sksamuel.scrimage.pixels.Pixel
import java.io.File
import java.lang.Math.pow

class Gauss {
    private fun gaussMatrix(kernelSize:Int=3, standardDeviation:Double=0.2): Array<Array<Double>> {
        val kernel = Array(kernelSize) { Array(kernelSize) { 0.0 } }

        val a = (kernelSize + 1) / 2
        val b = (kernelSize + 1) /2
        //Строим матрицу свёртки
        for(i in 0..<kernelSize) {
            for(j in 0..<kernelSize) {
                kernel[i][j] = gaussFunc(i, j, standardDeviation, a, b)
            }
        }
        print(kernel)
        print("//////////")
        var elementSum = 0.0
        kernel.forEach { it.forEach { el->elementSum+=el } }
        for(i in 0..<kernelSize) {
            for(j in 0..<kernelSize) {
                kernel[i][j] = kernel[i][j]/elementSum
            }
        }
        return kernel
    }
    private fun gaussFunc (x:Int, y:Int, omega:Double, a:Int, b:Int): Double {
        val omega2 = 2 * pow(omega,2.0)
        val m1 = 1 / (Math.PI * omega2)
        val m2 = Math.exp(-(Math.pow((x - a).toDouble(),2.0) + Math.pow((y - b).toDouble(),2.0) / omega2))
        return m1 * m2
    }
    fun gaussBlur(img: ImmutableImage, kernelSize:Int=3, standardDeviation:Double=0.2): ImmutableImage? {
        val kernel = gaussMatrix(kernelSize,standardDeviation)
        val imgBlur = img.copy()

        //Заводим стартовые индексы
        val xStart = kernelSize / 2
        val yStart = kernelSize / 2
        for(i in xStart..<imgBlur.height - xStart) {
            for (j in yStart..<imgBlur.width - yStart) {
                var r = 0.0
                var g = 0.0
                var b = 0.0

                // Применение ядра к соседним пикселям
                for (kx in -kernelSize / 2..kernelSize / 2) {
                    for (ky in -kernelSize / 2..kernelSize / 2) {
                        val pixelX = (i + kx).coerceIn(0, imgBlur.width - 1)
                        val pixelY = (j + ky).coerceIn(0, imgBlur.height - 1)

                        val pixelColor = imgBlur.pixel(pixelX, pixelY)
                        val weight = kernel[kx + kernelSize / 2][ky + kernelSize / 2]

                        r += pixelColor.red() * weight
                        g += pixelColor.green() * weight
                        b += pixelColor.blue() * weight
                    }
                }
                imgBlur.setPixel(
                    Pixel(
                        i,
                        j,
                        r.toInt().coerceIn(0, 255),
                        g.toInt().coerceIn(0, 255),
                        b.toInt().coerceIn(0, 255),
                        1
                    )
                )
            }
        }
        return imgBlur
    }
    fun BlurFuss(){
        val imageFile = File("src/main/resources/test2.jpg")
        val inputImage = ImmutableImage.loader().fromFile(imageFile)
        val resizedImage = inputImage.scaleTo(640, 640)
        val filtered = resizedImage.filter(GrayscaleFilter())
        val writer = JpegWriter()
        val kernel_size = 11
        val standard_deviation = 100.0
        val imgBlur1 = gaussBlur(filtered, kernel_size, standard_deviation)
        val resultFile = imgBlur1?.output(writer, File("src/main/resources/test4.jpg"))

    }

}