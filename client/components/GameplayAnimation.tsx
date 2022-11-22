import React from "react";
import styles from "../styles/Gameplay.module.css";
import EditionDropMetadata from "../lib/EditionDropMetadata";

const MineralGem = (
    <div className={styles.slide}>
        <img src="./mineral.png" height="48" width="48" alt='mineral-gem' />
    </div>
);

type Props = {
    multitool: EditionDropMetadata | undefined;
};

export default function GameplayAnimation({ multitool }: Props) {
    if(!multitool) { // If user doesn't have a multitool
        return <div style={{ marginLeft: 8 }}>I need a multitool!</div>
    };

    return (
        <div className={styles.slider}>
            <div className={styles.slideTrack}>
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
                {MineralGem}
            </div>
        </div>
    )
}