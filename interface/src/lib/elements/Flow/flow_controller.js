import * as PIXI from "pixi.js";
import { Application } from 'pixi.js';

/**
 * @typedef {import("$lib/relay_types/flow").Flow} Nodes
*  @typedef {import("$lib/relay_types/flow").Edges} Edges
*  @typedef {import("$lib/relay_types/flow").FlowEntry} Node
*  @typedef {Object.<string, Node>} NodeMap 
   
   
*   @typedef {"node.click" | "node.over" | "node.over.out"} MouseEventName
*   @typedef {Node & {x?:number,y?:number, size?:number, grids?:Object.<string, true>}} nodePosition

         
 **/


let _triangleGrphics = {};

/**
     * 
     * @param {{id?:any, color?:number, width?:number, height?:number| null}} param0
     * @returns {PIXI.Graphics} 
     */

function getTriangleShape({ id = null, color = 0xFF0000, width = 10, height = 10 }) {
    if (id) {
        if (id in _triangleGrphics) {
            const ret = _triangleGrphics[id].clone()
            ret.pivot.set(width / 2, height)
            return ret
        }
    }
    const graphics = new PIXI.Graphics()

    graphics.moveTo(0, height);
    graphics.lineTo(width / 2, 0);
    graphics.moveTo(width / 2, 0);
    graphics.lineTo(width, height);

    graphics.pivot.set(width / 2, height)
    graphics.stroke({ width: 1, color });
    if (id) {

        _triangleGrphics[id] = graphics;
    }
    return graphics











}


const defaultOptions = {
    edge: {
        width: 2,
        color: 0xdad7d7
    }
}


/**
 * 
 * @param {HTMLElement} container
 * @param {Partial<{[key:string]:any, edge:{color?:string, width?:number}}>} options 
 */
export async function FlowControllerBuilder(container, options = {}) {
    const app = new Application();
    const canvas = document.createElement('canvas');
    container.appendChild(canvas)
    await app.init({ canvas, antialias: true, backgroundAlpha: 0, resizeTo: container })
    let reset = async function () {

        container.removeChild(canvas)
        reset = null;
        return await FlowControllerBuilder(this.container, this.options)
    }
    reset = reset.bind(
        { container, options }
    );
    return [new FlowController(app, container, options), reset]
}
export class FlowController {
    /**
     * 
     * @param {Application} app
     * @param {HTMLElement} container 
     * @param {Partial<{[key:string]:any, edge:{color?:string, width?:number}, }>} options 
     */
    constructor(app, container, options = {}) {
        /**
         * @type {Application}
         */
        this.app = app
        this.app.stage.sortableChildren = true;
        this._gridMap = {};
        /**
         * @type {Object.<string, import("./Flow.event").IntaractiveData>}
         */
        this._interactiveGrid = {};
        this._gridStep = 5

        this._maxYear = -1;
        this._maxMonth = -1;

        this._minYear = Infinity;
        this._minMonth = Infinity
        this._ymdAdjast = 0



        this.options = Object.assign({}, defaultOptions, options)


        this.padding = 10;
        this._initTansform()
        this.centerV = this.app.screen.height / 2

        //centerScale.fill(0x994233);
        //centerScale.setStrokeStyle({ width: 4, color: 0xffd900 });

        // const wheelHandler = this.onZoom.bind(this)
        //container.addEventListener('wheel', wheelHandler)
        const onMouseEnter = this.onMouseEnter.bind(this);
        container.addEventListener('mouseenter', onMouseEnter);
        const onMouseDown = this.onMouseDown.bind(this)
        container.addEventListener('mousedown', onMouseDown)
        const onMouseMove = this.onMouseMove.bind(this)
        container.addEventListener('mousemove', onMouseMove)
        const onMouseUp = this.onMouseUp.bind(this)
        container.addEventListener('mouseup', onMouseUp)
        const onMouseOut = this.onMouseOut.bind(this);
        container.addEventListener('mouseout', onMouseOut)
        this._initEvent()
        this._scaleCache = {}

        this._offset = {
            x: container.parentElement.offsetLeft,
            y: container.parentElement.offsetTop
        }
        this._domContainer = container;

        //


        this.app.ticker.add(this.onTick.bind(this))
        this.app.ticker.start()



        this.zoomLevelStepRatio = 0.3;


        this._isOnDrag = false;
        this._isMouseEnter = false;
        this._isNodeOver = false





        this.centerHeight = container.clientHeight / 2
        this.dayStep = 30;
        this.dateDysplayLimit = 0.5;
        this.startMonth = 0
        this.startPosition = 10
        this._mousePosition = { x: 0, y: 0 };
        this._initContiners()
        this._initBackGroundScale();





        /**
         * 
         * @type {Object.<string, nodePosition>}        
         * */

        this._index = {};

        /**
         * @type {Object.<string, Object.<string, true>>}
         */
        this._edgeMaps = {}




        //this.setTransform({ scaleX: 1 / 30, scaleY: 1 / 30 })

        this._dragLimit = {
            x: {
                max: 0,
                min: 0
            },
            y: {
                max: 0,
                min: 0
            }
        }



    }
    /**
     * @param {MouseEventName} event
     * @param {Function} callback
     */
    on(event, callback) {
        const callbacks = this._events[event] || [];
        callbacks.push(callback);
        this._events[event] = callbacks

    }
    /**
     * @param {MouseEventName} event
     * @param {any} messages
     */
    _emit(event, ...messages) {
        const callbacks = this._events[event] || [];
        for (const callback of callbacks) {
            callback(...messages)
        }


    }
    /**
     * @param {string | number} nodeId
     */
    moveToNode(nodeId) {
        const node = this._index[nodeId];
        const [year, month, date] = FlowUtil.stringToYearMonthDate(node.published)
        this.moveToDate(year, month, date, true)
        return node

    }


    _initEvent() {
        this._events = {}
    }
    _initContiners() {
        this._frontContainer = new PIXI.Container()
        this._frontContainer.zIndex = 10;
        this.app.stage.addChild(this._frontContainer);
        this._graphContainer = new PIXI.Container();
        this._graphContainer.zIndex = 10;
        this._edgeContainer = new PIXI.Container();
        this._edgeContainer.zIndex = 0;
        this._edgeLineContainer = new PIXI.Container()
        this._edgeLineContainer.zIndex = 0;
        this._edgeContainer.addChild(this._edgeLineContainer)
        this._edgeArrowContainer = new PIXI.Container()
        this._edgeArrowContainer.zIndex = 10;
        this._edgeContainer.addChild(this._edgeArrowContainer)

        this._graphContainer.addChild(this._edgeContainer);
        this._vertexContainer = new PIXI.Container();
        this._vertexContainer.zIndex = 10;
        this._graphContainer.addChild(this._vertexContainer)
        this._graphContainer.sortableChildren = true;
        this._frontContainer.addChild(this._graphContainer)
        this._scaleContainer = new PIXI.Container()
        this._scaleContainer.zIndex = 0;
        this._frontContainer.addChild(this._scaleContainer)
        this._backgroundContainer = new PIXI.Container()
        this._backgroundContainer.zIndex = 0;
        this._backgroundContainer.sortableChildren = true;
        this.app.stage.addChild(this._backgroundContainer)
        this._dateScaleContainer = new PIXI.Container();
        this._dateScaleContainer.zIndex = 1
        this._backgroundContainer.addChild(this._dateScaleContainer)

    }

    _initTansform() {
        this._isTransformed = false;
        this._transforms = {
            x: 0,
            y: 0,
            scaleX: 1,
            scaleY: 1,
            deltaX: 0,

        }

    }
    /**
     * @param {{x?:number, y?:number, scaleX?:number, scaleY?:number, moveX?:number, moveY?:number}} arg 
     */
    setTransform(arg) {

        this._transforms.x = Math.min(this._dragLimit.x.max, Math.max(this._dragLimit.x.min, arg.x || this._transforms.x || 0 + arg.moveX || 0))
        this._transforms.y = Math.min(this._dragLimit.y.max, Math.max(this._dragLimit.y.min, arg.y || this._transforms.y || 0 + arg.moveY || 0))
        this._transforms.deltaX = arg.x || 0;


        /*const scaleX = this._transforms.scaleX + arg.scaleX || 0
        const scaleY = this._transforms.scaleY + arg.scaleY || 0
        



        if (arg.scaleX && scaleX >= 1 / 30 && arg.scaleY && scaleY >= 1 / 30) {
            this._transforms.scaleX = scaleX;
            this._transforms.scaleY = scaleY
            this._isTransformed = true;
        }
        */


        this._isTransformed = true;




    }

    /**
     * 
     * @param {WheelEvent} event 
     */
    onZoom(event) {
        event.preventDefault();
        const direction = event.deltaY >= 0 ? -1 : 1;
        let zoomDelta = direction * this.zoomLevelStepRatio;


        const scaleX = zoomDelta;
        const scaleY = zoomDelta;



        this.setTransform({ scaleX, scaleY })




    }
    onMouseEnter() {
        this._isMouseEnter = true
    }
    /**
     * 
     * @param {MouseEvent} event 
     */
    onMouseDown(event) {
        this._isOnDrag = true
        this._mousePosition = { x: event.clientX, y: event.clientY }
        this._emitNodeMouseInteraction('node.click', event);



    }

    /**
     * @param {MouseEventName} eventName
     * @param {MouseEvent} mouseEvent
     */
    _emitNodeMouseInteraction(eventName, mouseEvent) {
        const target_rect = this._domContainer.getBoundingClientRect();
        const x = (mouseEvent.clientX - target_rect.left - this._transforms.x) / this._transforms.scaleX
        const yCenter = this.app.screen.height / 2;
        const y = yCenter + (mouseEvent.clientY - target_rect.top - this._transforms.y - yCenter) / this._transforms.scaleY;


        const grid = this._getGridFromAxis(x, y);


        if (grid in this._interactiveGrid) {
            const interactiveData = this._interactiveGrid[grid]
            const rect = this._domContainer.getBoundingClientRect()
            const x = (interactiveData.x + this._transforms.x) / this._transforms.scaleX + rect.x + window.scrollX
            const y = (interactiveData.y + this._transforms.y) / this._transforms.scaleY + rect.y + window.scrollY
            /**
             * @type {import("./Flow.event").FlowNodeEventMessage}
             */
            const eventMessage = { x, y, interactiveData, mouseEvent }
            this._emit(eventName, eventMessage)


            return true
        }
        return false
    }
    onMouseOut() {
        this._isOnDrag = false;
        this._isMouseEnter = false;
        this._isNodeOver = false
    }
    onMouseUp() {
        this._isOnDrag = false;
    }
    /**
     * 
     * @param {MouseEvent} event 
     */
    onMouseMove(event) {

        if (this._isMouseEnter === true && this._isOnDrag === false) {
            const _isNodeOver = this._emitNodeMouseInteraction('node.over', event)
            if (_isNodeOver === false && this._isNodeOver === true) {
                this._emit("node.over.out")
            }
            this._isNodeOver = _isNodeOver
        }
        if (this._isOnDrag === false) {
            return
        }

        this.setTransform({
            moveX: event.clientX - this._mousePosition.x,
            moveY: event.clientY - this._mousePosition.y
        });
        this._mousePosition = { x: event.clientX, y: event.clientY }




    }
    /**
     * @param {number} year
     * @param {number} month
     * @param {number} date
     * @param {boolean} [isCenter=false] 
     */
    moveToDate(year, month, date, isCenter = true) {

        let x = -1 * this._computeXFromDate(year, month, date)


        if (isCenter === true) {
            x += this._domContainer.clientWidth / 2





        }
        this.setTransform({ x })




    }
    /**
     * @param {number} year
     * @param {number} month
     * @param {number} date
     */
    _getXFromYearMonthDate(year, month, date) {
        //  最小の年と同じ→最小の年の月の分のみ
        //  ↑でない→年の差分
        //  追加時→同じ式で補正分を算出
        let yearStep = year - this._minYear




        return (yearStep * 12 * 31 + (month - this._minMonth) * 31 + date) * this.dayStep + this._ymdAdjast;
        //return ((year - this._minYear) * 12 * 31 + (month - 1) * 31 + date) * 20;
    }
    destroy() {
        this.app.destroy()


        //this._domContainer.removeEventListener('wheel', this._wheelHandler)
        this._domContainer = null;


    }
    onTick() {
        if (this._isTransformed === false) {
            return
        }

        const yAdjast = this.app.screen.height / 2 * (1 - this._transforms.scaleY);

        this._graphContainer.updateTransform({ x: this._transforms.x, y: this._transforms.y + yAdjast, scaleX: this._transforms.scaleX, scaleY: this._transforms.scaleY })

        this._scaleContainer.position.set(this._transforms.x, this._scaleContainer.position.y)
        this._isTransformed = false;



        /**
         * @type {{scale:PIXI.Container; year:number; month:number;}[]}
         */
        const scales = this._yearMonthScales
        if (this._transforms.scaleX !== 1) {
            for (const { scale, year, month } of scales) {
                const newX = this._computeX(year, month, 0, this._transforms.scaleX)
                scale.position.set(newX, scale.position.y)

                if (newX + this._transforms.x < this.padding) {
                    scale.visible = false
                }
                else {
                    scale.visible = true
                }


            }
        }

        this._circulerDayScale()
    }
    _circulerDayScale() {
        /**
         * @type {PIXI.Graphics[]}
         */
        const keeps = [];
        /**
         * @type {PIXI.Graphics[]}
         */
        const circleArounds = [];
        const isLeft = this._transforms.deltaX < 0;
        const screenRight = this.app.screen.width - this.padding;
        const scaleX = this._transforms.scaleX;

        const padding = this.padding


        let count = 0;
        const step = this.dayStep * this._transforms.scaleX

        const adjest = this._transforms.x % step
        for (const dateScale of this._dateScales) {
            const x = count * step + adjest + padding
            count++;
            dateScale.position.set(x, dateScale.position.y)
            if (x < this.padding || x > screenRight) {

                dateScale.visible = false;

                circleArounds.push(dateScale)

                continue;

            }
            dateScale.visible = true;
            keeps.push(dateScale)

        }
        let startX;

        while (circleArounds.length > 0 && (keeps.length === 0 || keeps[keeps.length - 1].x < screenRight)) {

            const x = keeps.length * step + adjest + padding
            const circleAround = circleArounds.shift()
            circleAround.x = x;
            circleAround.visible = true;


            keeps.push(circleAround);

        }


        if (keeps.length === 0) {
            startX = padding;
        }
        else {
            const targetIndex = isLeft ? keeps.length - 1 : 0;
            startX = keeps[targetIndex].position.x
            if (targetIndex === 0) {
                startX -= circleArounds.length * step;
            }

        }

        count = 1;
        const directionX = isLeft === true ? 1 : -1;

        for (const circleAround of circleArounds) {
            const x = startX + this.dayStep * scaleX * count * directionX;

            circleAround.position.set(x, circleAround.position.y);
            count += 1;
        }
        if (isLeft === true) {
            this._dateScales = keeps.concat(circleArounds)
        }
        else {
            this._dateScales = circleArounds.concat(keeps)
        }





    }

    /**
     * @param {Nodes} nodes
     * @param {Edges} edges
     */
    setData(nodes, edges) {

        const { yearDiff, minYear, } = this.addNode(nodes, edges)

        this._createForegroundScale();
        this._createSubscale(minYear, yearDiff)


    }

    _createForegroundScale() {



        this._monthScaleContainer = new PIXI.Container();
        this._yearScaleContainer = new PIXI.Container()
        /**
         * @type {{ scale: PIXI.Container; month:number; year:number; }[]}
         */
        this._yearMonthScales = [];





        this._scaleContainer.addChild(this._yearScaleContainer, this._monthScaleContainer)
        /*const centerScale = new PIXI.Graphics()
        centerScale.setStrokeStyle({ width: 4, color: "#994233" });
        centerScale.moveTo(5, this.centerV);
        centerScale.lineTo(this.app.screen.width - 5, this.centerV);
        */
        //this._dateScaleContainer.addChild(centerScale);
        const centerScale = new PIXI.Graphics()
        centerScale.moveTo(5, this.centerV);

        centerScale.lineTo(this.app.screen.width - 5, this.centerV);

        centerScale.stroke({ width: 4, color: "#994233" });

        this._dateScaleContainer.addChild(centerScale)


    }
    _initBackGroundScale() {
        const repeatCount = this.app.screen.width / (this.dayStep / 3)


        /**
         * @type {PIXI.Graphics[]}
         */
        this._dateScales = []
        for (let index = 0; index < repeatCount; index++) {
            const x = index * this.dayStep + this.padding;

            const scale = this._createScale(x, 6, 'day')
            this._dateScaleContainer.addChild(scale)
            this._dateScales.push(scale)





        }



    }

    /**
     * @param {number} x
     * @param {number} lineHeight
     * @param {string} scaleType
     * @returns {PIXI.Graphics}
     
     */
    _createScale(x, lineHeight, scaleType) {

        if ((scaleType in this._scaleCache) === false) {

            const scale = new PIXI.Graphics()

            scale.moveTo(0, 5)
            scale.lineTo(0, 10 + lineHeight);
            scale.stroke({ width: 1, color: "#dad7d7" });
            /*scale.lineStyle(circleR + 1, 0xFFFFFF)
            scale.beginFill(0x994233);
            scale.drawCircle(0, this.centerV, 6);
            scale.endFill();
            */

            this._scaleCache[scaleType] = scale;

        }
        const clone = this._scaleCache[scaleType].clone()
        clone.position.set(x, 0);
        return clone;


    }
    /**
     * 
     * @param {number} minYear 
     * @param {number} yearDiff 
     */
    _createSubscale(minYear, yearDiff) {
        let scaleContainer;
        let lineHeight;
        const style = new PIXI.TextStyle({
            fontFamily: 'Arial',
            fontSize: 14,
            fill: '#000000',
        });
        for (let yearStep = 0; yearStep < yearDiff + 1; yearStep++) {
            const year = minYear + yearStep;
            let month = yearStep == 0 ? this._minMonth : 0
            while (month < 12) {

                const x = this._computeX(yearStep, month, 0, 1)


                let scaleType;
                if (month === 0) {
                    scaleType = 'year';

                    scaleContainer = this._yearScaleContainer;

                    lineHeight = 10;



                }
                else {
                    scaleType = 'month';
                    scaleContainer = this._monthScaleContainer
                    lineHeight = 8;

                }

                const scale = this._createScale(0, lineHeight, scaleType)
                const label = new PIXI.Text({ text: `${year}/${String(month + 1).padStart(2, '0')}`, style })
                label.position.set(5, 5)
                const wrapContainer = new PIXI.Container()

                wrapContainer.addChild(scale)
                wrapContainer.addChild(label)
                wrapContainer.position.set(x, this.app.screen.height - 15 - lineHeight);
                scaleContainer.addChild(wrapContainer)
                this._yearMonthScales.push({ scale: wrapContainer, year: yearStep, month });
                month++;
            }

        }

    }
    /**
     * @param {number} year
     * @param {number} month
     * @param {number?} date
     * @param {number} scaleRatio
     */
    _computeXFromDate(year, month, date = 0, scaleRatio = 1) {
        return this._computeX(year - this._minYear, month, date, scaleRatio)
    }

    /**
     * @param {number} yearDiff
     * @param {number} month
     * @param {number?} date
     * @param {number} scaleRatio
     */
    _computeX(yearDiff, month, date = 0, scaleRatio = 1) {
        return (yearDiff * 31 * 12 + (month - this._minMonth) * 31 + date) * this.dayStep * scaleRatio + this.padding
    }
    /**
     
     * @param {Nodes} nodes 
     * @param {Edges} edges 
     */
    addNode(nodes, edges) {

        let total = 0;
        const weights = [];

        let maxYear = this._maxYear || 0;

        let minYear = this._minYear;
        let minMonth = this._minMonth;
        /**
         * @type {{year:number, month:number, date:number}[]}
         *  */
        const yearMonthDates = [];
        const pt = /\d+/g

        for (const node of nodes) {
            this._index[node.id] = node;

            total += node.weight;
            weights.push(node.weight)



            let [year, month, date] = Array.from(node.published.matchAll(pt)).map(Number);
            month -= 1
            if (year > maxYear) {
                maxYear = year;
            }

            if (year <= minYear) {
                minYear = year;
                if (minMonth > month) {
                    minMonth = month;
                }

            }
            yearMonthDates.push({ year, month, date })

        }
        if (this._minYear >= minYear) {
            this._minYear = minYear
            if (this._minMonth > minMonth) {
                this._minMonth = minMonth
            }
        }

        if (maxYear > this._maxYear) {
            this._maxYear = maxYear;
        }

        const yearDiff = maxYear - minYear || 1;
        const avg = total / nodes.length
        const sigma = Math.sqrt(weights.reduce(function (prev, cur) {
            return prev + Math.pow(cur - avg, 2)

        }, 0) / nodes.length)


        /**
         * @type {[Node, {year:number,month:number, date:number}, number][]}
         */
        const nodeDatas = weights.map(function (weight, index) {
            const reguraizedWeight = sigma === 0 ? 1 : (weight - avg) / sigma;

            return [nodes[index], yearMonthDates[index], (Math.tanh(reguraizedWeight / 2) + 1) / 2]

        });
        /**
         * @type {Object.<string, PIXI.Graphics>}
         */

        const nodeGraphics = {};




        for (const [node, yearMonthDate, weight] of nodeDatas) {
            const size = (5 + 15 * weight) / 2;




            //当たり判定と重複処理
            let x = this._computeX(yearMonthDate.year - this._minYear, yearMonthDate.month, yearMonthDate.date);

            let y = (1 - node.y) * this.app.screen.height / 2;







            const end = y + size;
            let _y = y - size;
            /**
             * @type {Object.<string, true>}
             */
            const grids = {};
            while (_y <= end) {
                const grid = this._getGrid(yearMonthDate.year, yearMonthDate.month, yearMonthDate.date, _y);

                _y += this._gridStep;
                grids[grid] = true


                const interactiveData = this._interactiveGrid[grid] || {
                    nodes: [],
                    isOverwraped: false,
                    x: x,
                    y: 0,
                    maxWeight: -1



                }

                if (interactiveData.isOverwraped === false) {
                    interactiveData.isOverwraped = grid in this._interactiveGrid;
                }
                if (interactiveData.maxWeight < weight) {
                    interactiveData.y = y
                    interactiveData.maxWeight = node.weight
                    interactiveData.nodes.unshift(node)
                }
                else {
                    interactiveData.nodes.push(node)
                }
                this._interactiveGrid[grid] = interactiveData

            }
            x += size * 0.5
            y += size * 0.5
            this._index[node.id] = Object.assign(node, { x, y, size, grids })

            //@todo 中心を基準に並び順を変更
            //@task ズームした時の大きさを変わらないように(保留。年モード→月モード→日モード(チャットのみ?))
            const graphic = new PIXI.Graphics()

            graphic.circle(x, y, size);

            graphic.fill("#0683c9ff")



            nodeGraphics[node.id] = graphic





        }


        const nodeGraphicsArr = Array.from(Object.values(nodeGraphics))

        if (nodeGraphicsArr.length > 0) {
            this._vertexContainer.addChild(...Array.from(Object.values(nodeGraphics)))

        }





        const edgeLines = [];
        const edgeArrows = [];

        for (const edge of edges) {
            /**
             * @type {nodePosition}
             */
            const fromData = this._index[edge.from]
            /**
             * @type {nodePosition}
             */
            const toData = this._index[edge.to]
            if (!fromData || !toData) {
                continue;
            }

            let isColide = false;
            for (const grid of Object.keys(fromData.grids)) {
                if (toData.grids[grid] === true) {
                    isColide = true;
                    break;
                }
            }
            if (isColide === true) {
                continue;
            }
            let isEdgeExist = false;
            let isReverseEdge = false;
            for (const fromGrid in fromData.grids) {
                let edgeMap = this._edgeMaps[fromGrid] || {};
                for (const toGrid in toData.grids) {
                    isEdgeExist = isEdgeExist || edgeMap[toGrid] == true;
                    isReverseEdge = isReverseEdge || (this._edgeMaps[toGrid] || {})[fromGrid] == true;
                    isEdgeExist = isEdgeExist || isReverseEdge
                    edgeMap[toGrid] = true;
                }
                this._edgeMaps[fromGrid] = edgeMap
            }
            if (isEdgeExist === true && isReverseEdge === false) {
                continue;
            }





            const vecX = toData.x - fromData.x;
            const vecY = toData.y - fromData.y;
            const vecLength = (vecX ** 2 + vecY ** 2) ** 0.5
            const toGap = toData.size + 15
            const toX = toData.x - vecX * toGap / vecLength;
            const toY = toData.y - vecY * toGap / vecLength;
            const antiLock = toData.y > fromData.y ? -1 : 1
            const ang = antiLock * Math.acos((toData.x - fromData.x) / vecLength);

            //PIXI のメッシュの座標系は右上起点。回転は時計回り
            //メッシュの底、左右中央をpivotに。90度回転して接続して向きを線の角度に



            const fromGap = fromData.size + 5
            const fromX = fromData.x + vecX * fromGap / vecLength
            const fromY = fromData.y + vecY * fromGap / vecLength



            const triangle = getTriangleShape({ id: 'santri' })

            triangle.position.set(toX, toY)

            if (isEdgeExist === false) {
                const line = new PIXI.Graphics();

                line.moveTo(fromX, fromY)
                line.lineTo(toX, toY);
                line.stroke({ width: this.options.edge.width || 2, color: this.options.edge.color || "#1ac379ff" });
                edgeLines.push(line);


            }

            const triAng = ang - Math.PI / 2;
            triangle.rotation -= triAng;
            edgeArrows.push(triangle)




        }
        if (edgeLines.length > 0) {
            this._edgeLineContainer.addChild(...edgeLines)
        }
        if (edgeArrows.length > 0) {
            this._edgeArrowContainer.addChild(...edgeArrows)
        }

        const domContanerRect = this._domContainer.getBoundingClientRect()
        this._dragLimit.x.min = Math.min(0, domContanerRect.width - this._computeX(this._maxYear - this._minYear, this._maxMonth + 1))
        this.isDraggable = this._dragLimit.x.min < 0 || this._dragLimit.x.max > 0
        return { nodeGraphics, yearDiff, minYear, minMonth };







    }
    /**
     * @param {number} x
     * @param {number} y
     */
    _getGridFromAxis(x, y) {
        const baseX = (x - this.padding) / this.dayStep;
        const yearDiff = 12 * 31;
        const monthDiff = 31;
        let year = Math.floor(baseX / yearDiff) + this._minYear;
        let month = Math.ceil(Math.abs(baseX % yearDiff) / 31) + this._minMonth - 1;
        year += Math.floor(month / 12)
        month = month % 12

        const date = Math.floor(Math.abs(baseX % yearDiff) % monthDiff);
        //console.log(year, month, date)

        return this._getGrid(year, month, date, y);


    }
    /**
     * @param {number} year
     * @param {number} month
     * @param {number} date
     * @param {number} y
     */
    _getGrid(year, month, date, y) {
        return [year, month, date, Math.floor(y / 5)].join('_');
    }


}

const numberPt = /\d+/g
export const FlowUtil = {
    /**
     * 
     * @param {string} dateString 
     * @returns 
     */
    stringToYearMonthDate: function (dateString) {
        return Array.from(dateString.matchAll(numberPt)).map(Number)
    }
}