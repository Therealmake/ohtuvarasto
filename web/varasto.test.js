const Varasto = require('./varasto');

describe('Varasto', () => {
    test('constructor creates empty warehouse', () => {
        const v = new Varasto(10);
        expect(v.saldo).toBe(0);
        expect(v.tilavuus).toBe(10);
    });

    test('negative capacity is set to zero', () => {
        const v = new Varasto(-1);
        expect(v.tilavuus).toBe(0.0);
    });

    test('negative initial stock is set to zero', () => {
        const v = new Varasto(10, -1);
        expect(v.saldo).toBe(0.0);
    });

    test('initial stock exceeding capacity is capped', () => {
        const v = new Varasto(10, 15);
        expect(v.saldo).toBe(10.0);
    });

    test('lisaaVarastoon adds to stock', () => {
        const v = new Varasto(10);
        v.lisaaVarastoon(8);
        expect(v.saldo).toBe(8);
    });

    test('lisaaVarastoon with negative amount does nothing', () => {
        const v = new Varasto(10);
        v.lisaaVarastoon(-3);
        expect(v.saldo).toBe(0.0);
    });

    test('lisaaVarastoon caps at capacity', () => {
        const v = new Varasto(10, 9);
        v.lisaaVarastoon(5);
        expect(v.saldo).toBe(10.0);
    });

    test('paljonkoMahtuu returns available space', () => {
        const v = new Varasto(10);
        v.lisaaVarastoon(8);
        expect(v.paljonkoMahtuu()).toBe(2);
    });

    test('otaVarastosta returns correct amount', () => {
        const v = new Varasto(10);
        v.lisaaVarastoon(8);
        const taken = v.otaVarastosta(2);
        expect(taken).toBe(2);
        expect(v.saldo).toBe(6);
    });

    test('otaVarastosta with negative amount returns zero', () => {
        const v = new Varasto(10, 5);
        const taken = v.otaVarastosta(-2);
        expect(taken).toBe(0.0);
        expect(v.saldo).toBe(5.0);
    });

    test('otaVarastosta more than stock returns all available', () => {
        const v = new Varasto(10, 4);
        const taken = v.otaVarastosta(10);
        expect(taken).toBe(4.0);
        expect(v.saldo).toBe(0.0);
    });

    test('toString returns correct format', () => {
        const v = new Varasto(10, 3);
        expect(v.toString()).toBe('saldo = 3, vielä tilaa 7');
    });

    test('toJSON returns correct object', () => {
        const v = new Varasto(10, 3);
        const json = v.toJSON();
        expect(json.tilavuus).toBe(10);
        expect(json.saldo).toBe(3);
        expect(json.paljonkoMahtuu).toBe(7);
    });
});
