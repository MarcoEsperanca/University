// #import "@preview/algo:0.3.3": algo, i, d, comment, code
#import "@preview/tablex:0.0.5": vlinex, hlinex
#let project(fontsize:11pt, doc) ={
  let calculated_leading = 10.95pt
  set heading(
    bookmarked: true,
    numbering: "1.1."
  )
  set text(
    font: "Times New Roman",
    size: fontsize,
    hyphenate: true,
    lang: "pt",
    region: "pt"
  )
  set page(
    numbering: "1 / 1",
    margin: (left: 12mm, right: 12mm, top: 13mm, bottom: 13mm)
  )
  set par(
    justify: true,
    leading: calculated_leading, // calculo manual
    first-line-indent: 1cm,
  )
  show par: set block(spacing: 21pt)
  set math.equation(
    numbering: "(1)"
  )
  show ref: it => {
    let eq = math.equation
    let el = it.element
    if el != none and el.func() == eq {
      numbering(
        el.numbering,
        ..counter(eq).at(el.location())
      )
    } else {
      it
    }
  }
  show figure.where(
    kind: table
  ): set figure.caption(position: top)
  show figure.caption: set text(size: fontsize - 2pt)
  // set algo() // not an element func yet (cause it's not possible on 0.8)
  show figure.where(
    kind: grid
  ): set figure(kind: image) // n funciona n sei pq

  //set figure(placement: auto)
  show figure.where(
    kind: "Algoritmo"
  ): set figure(placement: none) // juro que nao percebo pq e q isto n funciona
  set list(indent: 0.6cm)
  doc
}

#let vline(start:none, end:none) = {
  vlinex(start:start, end:end, stroke:0.5pt)
}

#let hline(start:none, end:none) = {
  hlinex(start:start, end:end, stroke:0.5pt)
}

#let hline_header(start:none, end:none) = {
  hlinex(start:start, end:end, stroke:0.5pt, expand:-3pt)
}

#let hline_before(start:none, end:none) = {
  // hlinex(start:start, end:end, stroke:0.5pt, expand:-3pt)
}
