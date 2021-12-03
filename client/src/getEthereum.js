export const getEthereum = async () => {

    // event listener is not reliable
    while (document.readyState !== "complete") {
        await new Promise(resolve => setTimeout(resolve, 50))
    }

    return window.ethereum

}
