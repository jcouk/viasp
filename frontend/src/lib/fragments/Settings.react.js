import React, {useState} from "react";
import {useColorPalette} from "../contexts/ColorPalette";
import {useHighlightedSymbol} from "../contexts/HighlightedSymbol";
import './settings.css'
import { darken } from 'polished';


function makeClassNameFromMarkedSymbol(highlightedSymbol) {
    let className = `noselect toggle_part unselected ${highlightedSymbol.length === 0 ? "fadeOut" : "fadeIn"}`;
    return className;
}

function ClearMarked() {
    const { highlightedSymbol, setHighlightedSymbol } = useHighlightedSymbol()
    const colorPalette = useColorPalette();
    const className = makeClassNameFromMarkedSymbol(highlightedSymbol)
    const [isHovered, setIsHovered] = useState(false);
    const [isClicked, setIsClicked] = useState(false);

    const hoverFactor = 0.08;
    const style = {
        background: colorPalette.explanationSuccess,
        color: colorPalette.dark,
        border: `1px solid ${colorPalette.dark}`,
    };

    if (isHovered) {
        style.background = darken(hoverFactor, style.background);
    }
    if (isClicked) {
        style.background = colorPalette.infoBackground;
    }

    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);
    const handleMouseDown = () => setIsClicked(true);
    const handleMouseUp = () => setIsClicked(false);

    return <span onClick={() => setHighlightedSymbol([])}
                className={className}
                style={style}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}>
            clear marked symbols</span>
}

export default function Settings() {

    return <div className="settings noselect" >
                <ClearMarked/>
            </div>
}
