declare module 'react-cytoscapejs' {
  import { Component, CSSProperties } from 'react'

  const CytoscapeComponent: Component<{
    elements: any
    stylesheet?: any[]
    layout?: any
    style?: CSSProperties
    cy?: (cy: any) => void
  }>

  export default CytoscapeComponent
}
