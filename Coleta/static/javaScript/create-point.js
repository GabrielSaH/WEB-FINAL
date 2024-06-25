function populateUFs() {
    const ufSelect = document.querySelector("select[name=uf]")
    fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    .then( res => res.json())
    .then( states => {
        
        for(state of states){
            ufSelect.innerHTML += `<option value="${state.id}">${state.nome}</option>`
        }

        

    })
}

populateUFs()

function getCities(event){
    const citySelect = document.querySelector("[name=city]")  
    const stateInput = document.querySelector("[name=state]")  

    const ufvalue = event.target.value

    const indexOfSelectedState = event.target.selectedIndex
    stateInput.value = event.target.options[indexOfSelectedState].text

    const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${ufvalue}/municipios`

    citySelect.innerHTML = "<option value>Selecione a Cidade</option>" //Limpa o campo cidades
    citySelect.disabled = true

    fetch(url) //procurar as cidades
    .then( res => res.json())
    .then( cities => {
        
        
        for(city of cities){
            citySelect.innerHTML += `<option value="${city.nome}">${city.nome}</option>`
        }

        citySelect.disabled = false
    })
}


document
    .querySelector("select[name=uf]")
    .addEventListener("change", getCities)


//itens de coleta
//todos os li
const itemsToCollect = document.querySelectorAll(".items-grid li")

for(const item of itemsToCollect) {
    item.addEventListener("click", handleSelectedItem)
}

const collectedItems = document.querySelector("input[name=items]")


let selectedItems = []
function handleSelectedItem(event){
    //adicionar ou remover uma classe com o js

    const itemLi = event.target
    itemLi.classList.toggle("selected") //toggle para adicionar ou remover

    const itemId = itemLi.dataset.id //pega os números que estão no id

    //verificar se existem items selecionados, se sim pegar os itens selecionados
    const alreadySelected = selectedItems.findIndex( item => {  //verifica se o item já está selecionado
        const itemFound = item == itemId //retornará um lógico
        return itemFound
     })

    //se já estiver selecionado, tirar da seleção.
    if(alreadySelected >= 0 ){  //tem o índice do material de coleta selecionado
        //tirar da seleção
        const filteredItems = selectedItems.filter( item => {
            const itemIsDifferent = item != itemId  //falso
            return itemIsDifferent
        })

        selectedItems = filteredItems
    } else {  
        //se não estiver selecionado, adicionar à seleção
        selectedItems.push(itemId)  //push - adicionar
    }

    //console.log(selectedItems)

   collectedItems.value = selectedItems

    //atualizar o campo escondido com os itens selecionados
}