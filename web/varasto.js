class Varasto {
    constructor(tilavuus, alkuSaldo = 0) {
        if (tilavuus > 0.0) {
            this.tilavuus = tilavuus;
        } else {
            this.tilavuus = 0.0;
        }

        if (alkuSaldo < 0.0) {
            this.saldo = 0.0;
        } else if (alkuSaldo <= this.tilavuus) {
            this.saldo = alkuSaldo;
        } else {
            this.saldo = this.tilavuus;
        }
    }

    paljonkoMahtuu() {
        return this.tilavuus - this.saldo;
    }

    lisaaVarastoon(maara) {
        if (maara < 0) {
            return;
        }
        if (maara <= this.paljonkoMahtuu()) {
            this.saldo = this.saldo + maara;
        } else {
            this.saldo = this.tilavuus;
        }
    }

    otaVarastosta(maara) {
        if (maara < 0) {
            return 0.0;
        }
        if (maara > this.saldo) {
            const kaikkiMitaVoidaan = this.saldo;
            this.saldo = 0.0;
            return kaikkiMitaVoidaan;
        }
        this.saldo = this.saldo - maara;
        return maara;
    }

    toString() {
        return `saldo = ${this.saldo}, vielä tilaa ${this.paljonkoMahtuu()}`;
    }

    toJSON() {
        return {
            tilavuus: this.tilavuus,
            saldo: this.saldo,
            paljonkoMahtuu: this.paljonkoMahtuu()
        };
    }
}

module.exports = Varasto;
