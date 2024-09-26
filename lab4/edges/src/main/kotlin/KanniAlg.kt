package org.example

import com.sksamuel.scrimage.ImmutableImage
import com.sksamuel.scrimage.filter.GrayscaleFilter
import com.sksamuel.scrimage.nio.JpegWriter
import com.sksamuel.scrimage.pixels.Pixel
import java.io.File
import kotlin.math.max

class KanniAlg {
    fun processImage(path: String, kernelSize: Int = 5, sigma: Double = 10.0, sizeX: Int = 640, sizeY: Int = 640) {
        val imageFile = File(path)
        val inputImage = ImmutableImage.loader().fromFile(imageFile)
        val resizedImage = inputImage.scaleTo(sizeX, sizeY)
        val filtered = resizedImage.filter(GrayscaleFilter())
        val writer = JpegWriter()
        val resultFile = filtered?.output(writer, File("src/main/resources/grayScale.jpg"))

        val blurredImage = Gauss().gaussBlur(filtered, kernelSize, sigma)
        blurredImage.output(writer, File("src/main/resources/gauss.jpg"))
        val grads = calcGradients(blurredImage)
        println(grads)
        val lengths = caclGradLengths(blurredImage, grads)
        println(lengths)
        val corners = calcCorners(blurredImage, grads)
        println(corners)

        val suppressedImg = supressNotMax(lengths, corners)
//        suppressedImg.output(writer,"src/main/resources/supressedImg.jpg")

        val edgeImg = checkThreshAndEdge(blurredImage, suppressedImg, lengths, 10)
        edgeImg?.output(writer, "src/main/resources/edgeImg.jpg")
        println(edgeImg)
    }

    fun pixelGray(inp: Pixel) = inp.toRGB()[0];

    fun calcGradients(img: ImmutableImage): MutableList<MutableList<Pair<Int, Int>>> {
        val gradientMatrix = mutableListOf<MutableList<Pair<Int, Int>>>();
        for (x in 1..<img.height - 1) {
            val matrixRow = mutableListOf<Pair<Int, Int>>();
            for (y in 1..<img.width - 1) {
                val Gx = -pixelGray(img.pixel(x - 1, y - 1)) - 2 * pixelGray(img.pixel(x, y - 1)) - pixelGray(
                    img.pixel(
                        x + 1,
                        y - 1
                    )
                ) + pixelGray(img.pixel(x - 1, y + 1)) + 2 * pixelGray(img.pixel(x, y + 1)) + pixelGray(
                    img.pixel(
                        x + 1,
                        y + 1
                    )
                )
                val Gy = -pixelGray(img.pixel(x - 1, y - 1)) - 2 * pixelGray(
                    img.pixel(
                        x - 1,
                        y
                    )
                ) - pixelGray(img.pixel(x - 1, y + 1)) + pixelGray(
                    img.pixel(
                        x + 1,
                        y - 1
                    )
                ) + 2 * pixelGray(img.pixel(x + 1, y)) + pixelGray(img.pixel(x + 1, y + 1))
                matrixRow.add(Pair<Int, Int>(Gx, Gy))
            }
            gradientMatrix.add(matrixRow)
        }
        return gradientMatrix
    }

    fun caclGradLengths(
        img: ImmutableImage,
        grads: MutableList<MutableList<Pair<Int, Int>>>
    ): MutableList<MutableList<Double>> {
        val res = mutableListOf<MutableList<Double>>();
        for (i in 0..<img.height) {
            val row = mutableListOf<Double>()
            for (i in 0..<img.width) {
                row.add(0.0)
            }
            res.add(row)
        }
        var k = 0
        for (i in 1..<img.height - 1) {
            var l = 0
            for (j in 1..<img.width - 1) {
                res[i][j] = Math.sqrt(
                    Math.pow(grads[k][l].first.toDouble(), 2.0) + Math.pow(
                        grads[k][l].second.toDouble(),
                        2.0
                    )
                )
                l = l + 1
            }
            k = k + 1
        }
        return res
    }

    fun calcCorner(grad: Pair<Int, Int>): Int {
        val tang = if (grad.first != 0) grad.second / grad.first else 999
        if (grad.first > 0 && grad.second < 0 && tang < -2.414 || grad.first < 0 && grad.second < 0 && tang > 2.414)
            return 0
        else if (grad.first > 0 && grad.second < 0 && tang < -0.414)
            return 1
        else if (grad.first > 0 && grad.second < 0 && tang > -0.414 || grad.first > 0 && grad.second > 0 && tang < 0.414)
            return 2
        else if (grad.first > 0 && grad.second > 0 && tang < 2.414)
            return 3
        else if (grad.first > 0 && grad.second > 0 && tang > 2.414 || grad.first < 0 && grad.second > 0 && tang < -2.414)
            return 4
        else if (grad.first < 0 && grad.second > 0 && tang < -0.414)
            return 5
        else if (grad.first < 0 && grad.second > 0 && tang > -0.414 || grad.first < 0 && grad.second < 0 && tang < 0.414)
            return 6
        else if (grad.first < 0 && grad.second < 0 && tang < 2.414)
            return 7
        if (grad.first == 0) {
            if (grad.second > 0)
                return 4
            return 0
        } else {
            if (grad.second > 0)
                return 2
            return 6
        }

    }


    fun calcCorners(
        img: ImmutableImage,
        grads: MutableList<MutableList<Pair<Int, Int>>>
    ): MutableList<MutableList<Int>> {
        val corners = mutableListOf<MutableList<Int>>();
        for (i in 0..<img.height) {
            val row = mutableListOf<Int>()
            for (i in 0..<img.width) {
                row.add(0)
            }
            corners.add(row)
        }
        var k = 1
        for (i in 0..<grads.size) {
            var l = 1
            for (j in 0..<grads[i].size) {
                corners[k][l] = calcCorner(grads[i][j])
                l = l + 1
            }
            k = k + 1
        }

        return corners
    }


    fun supressNotMax(
        gradsLenths: MutableList<MutableList<Double>>,
        corners: MutableList<MutableList<Int>>
    ): MutableList<MutableList<Int>> {
        val height = gradsLenths.size
        val width = gradsLenths[0].size
        val suppressed = mutableListOf<MutableList<Int>>();
        for (i in 0..<height) {
            val row = mutableListOf<Int>()
            for (i in 0..<width) {
                row.add(0)
            }
            suppressed.add(row)
        }

        for (y in 1..<height - 1) {
            for (x in 1..<width - 1) {
                val angle = corners[x][y]
                var q: Double = 0.0
                var r: Double = 0.0
                if (angle == 0 || angle == 4) {
                    q = gradsLenths[x + 1][y]
                    r = gradsLenths[x - 1][y]
                } else if (angle == 1 || angle == 5) {
                    q = gradsLenths[x - 1][y + 1]
                    r = gradsLenths[x + 1][y - 1]
                } else if (angle == 2 || angle == 6) {
                    q = gradsLenths[x][y + 1]
                    r = gradsLenths[x][y - 1]
                } else if (angle == 3 || angle == 7) {
                    q = gradsLenths[x + 1][y + 1]
                    r = gradsLenths[x - 1][y - 1]
                }

                if (gradsLenths[x][y] >= q && gradsLenths[x][y] >= r)
                    suppressed[x][y] = 255
                else
                    suppressed[x][y] = 0
            }
        }
        return suppressed
    }

    fun checkThreshAndEdge(
        img: ImmutableImage,
        suppressed: MutableList<MutableList<Int>>,
        gradientsLength: MutableList<MutableList<Double>>,
        boundPath1: Int = 10,
        boundPath2: Int = 25
    ): ImmutableImage? {
        var maxGradient = 0.0
        for(row in gradientsLength){
            for(j in row ){
                maxGradient = max(j,maxGradient)
            }
        }
        println(maxGradient)
        val lowerBound = maxGradient / boundPath1
        val upperBound = maxGradient / boundPath2

        val imgBorderFilter = img.copy();
        for (i in 0..<imgBorderFilter.height) {
            for (j in 0..<imgBorderFilter.width) {
                imgBorderFilter.setPixel(Pixel(i, j, 0, 0, 0, 1))
            }
        }
        for (i in 0..<img.height) {
            for (j in 0..<img.width) {
                val gradient = gradientsLength[i][j]
                if (suppressed[i][j] == 255) {
                    if (gradient in lowerBound..upperBound) {
                        var flag = false
                        for (k in -1..<2) {
                            for (l in -1..<2) {
                                if (flag) break
                                if (suppressed[i + k][j + l] == 255 && suppressed[i + k][j + l] >= lowerBound) {
                                    flag = true
                                    break
                                }
                            }
                        }
                        if (flag) {
                            suppressed[i][j] = 255
                        }
                    }
                    else if (gradient > upperBound) imgBorderFilter.setPixel(Pixel(i, j, 255, 255, 255, 1))
                    else imgBorderFilter.setPixel(Pixel(i, j, 0, 0, 0, 0))
                    }
            }
        }

            return imgBorderFilter
        }
    }
