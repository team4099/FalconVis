import { Modal } from "../lib/components/Modal.js"
import { GraphManager } from "../lib/components/GraphManager.js"

var setTeams = () => {
    blue = [
        parseInt(document.getElementById("blue1").value),
        parseInt(document.getElementById("blue2").value),
        parseInt(document.getElementById("blue3").value),
    ]

    red = [
        parseInt(document.getElementById("red1").value),
        parseInt(document.getElementById("red2").value),
        parseInt(document.getElementById("red3").value),
    ]

    graphContainerBlue.pushEditAll(blue)
    graphContainerRed.pushEditAll(red)
}
var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
var graphContainerRed = new GraphManager()
var graphContainerBlue = new GraphManager()

var red = [9999, 9999, 9999]
var blue = [9999, 9999, 9999]

export { setTeams, modal, graphContainerRed, graphContainerBlue, red, blue }