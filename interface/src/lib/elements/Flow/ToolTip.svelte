<script>
  import { onMount, tick } from "svelte";

  let message;
  let top = 0;
  let left = 0;

  let isVisible = false;
  let style = "";

  export function show(_left, _top, _message) {
    message = _message;
    top = _top;

    left = _left;
    isVisible = true;

    setTimeout(function () {
      for (const [direction, func] of Object.entries(arrowDirections)) {
        if (func() === true) {
          arrowDirection = direction;
          break;
        }
      }
      style = `top:${_framePosition.top}px; left:${_framePosition.left}px`;
    }, 0);
  }
  export function hide() {
    _framePosition = { top: -10000, left: -10000 };
    isVisible = false;
  }

  let _framePosition = { top: 0, left: 0 };

  /**
   * @type {HTMLElement}
   */
  export let flowElement;
  /**
   * @type {HTMLElement}
   */
  let frameElement;
  let tip;
  /**
   * @typedef {"left" | "right" | "top" | "down"} ArrowDirection
   * @type {ArrowDirection}
   */
  let arrowDirection = "down";
  /**
   * @type {HTMLElement}
   */
  let arrowElement;
  const maxRadius = 15;
  const padding = 10;

  /**
   * @type {Object.<ArrowDirection, Function>}
   */
  const arrowDirections = {
    left: function () {
      if (
        left - frameElement.getBoundingClientRect().width / 2 <
        flowElement.offsetLeft
      ) {
        _framePosition.top = top;

        _framePosition.left = left + maxRadius + padding;
        return true;
      }
      return false;
    },
    right: function () {
      if (
        left + frameElement.getBoundingClientRect().width / 2 >
        flowElement.offsetLeft + flowElement.getBoundingClientRect().width
      ) {
        _framePosition.top =
          top - frameElement.getBoundingClientRect().height / 2;
        _framePosition.left =
          left -
          (maxRadius + padding) -
          frameElement.getBoundingClientRect().width;
        return true;
      }
      return false;
    },
    up: function () {
      if (
        top -
          (maxRadius + padding) -
          frameElement.getBoundingClientRect().height -
          arrowElement.clientHeight <
        flowElement.offsetTop
      ) {
        _framePosition.top =
          top + (maxRadius + padding) + arrowElement.clientHeight;

        _framePosition.left =
          left - frameElement.getBoundingClientRect().width / 2;
        return true;
      }
      return false;
    },
    down: function () {
      _framePosition.top =
        top -
        (maxRadius + padding) -
        frameElement.getBoundingClientRect().height;

      _framePosition.left =
        left - frameElement.getBoundingClientRect().width / 2;

      return true;
    },
  };

  onMount(function () {
    const body = Array.from(document.getElementsByTagName("body"))[0];

    body.appendChild(frameElement);
  });
</script>

<div
  class:hidden={isVisible === false}
  class:visible={isVisible === true}
  class="tooltip-frame"
  bind:this={frameElement}
  {style}
>
  <div class="text-white bg-black p-2 fs-6" bind:this={flowElement}>
    {message}
  </div>
  <div
    class="bg-black arrow"
    bind:this={arrowElement}
    class:up={arrowDirection === "up"}
    class:down={arrowDirection === "down"}
    class:right={arrowDirection === "right"}
    class:left={arrowDirection === "left"}
  />
</div>

<style>
  .visible {
    position: absolute;
    text-align: center;
    display: block;
  }
  .hidden {
    visibility: hidden;
  }
  .tooltip-frame {
    position: absolute;
    width: fit-content;
    display: block;
  }

  .arrow {
    position: absolute;
    width: 0.8em;
    height: 0.8em;
  }

  .up {
    clip-path: polygon(50% 0, 100% 100%, 0 100%);
    top: -0.8em;
    left: calc(50% - 0.4em);
  }
  .right {
    clip-path: polygon(0 0, 100% 50%, 0 100%);
    top: calc(50% - 0.4em);
    left: 100%;
  }

  .down {
    clip-path: polygon(0 0, 100% 0, 50% 100%);
    top: 100%;
    left: calc(50% - 0.4em);
  }

  .left {
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
    top: calc(50% - 0.4em);
    left: -0.4em;
  }
</style>
