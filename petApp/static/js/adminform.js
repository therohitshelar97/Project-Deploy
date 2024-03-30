function Category(){
    var dog = document.getElementById('category').value;
    console.log(dog)
    // var cat = document.getElementById('category').value;
    // var parrot = document.getElementById('category').value;
    if(dog=='dog'){
        const op1 = document.getElementById('op1')
        op1.innerHTML = 'German Shepherds'
        op1.setAttribute('value','german shepherd')

        const op2 = document.getElementById('op2')
        op2.innerHTML = 'Bull Dog'
        op2.setAttribute('value','bulldog')

        const op3 = document.getElementById('op3');
        op3.innerHTML = 'Labrador Retriever'
        op3.setAttribute('value','labrador retriever')

        const op4 = document.getElementById('op4');
        op4.innerHTML = 'Golden Retriever'
        op4.setAttribute('value','golden retriever')

    }

    else if(dog=='cat'){
        const op1 = document.getElementById('op1')
        op1.innerHTML = 'Rag Doll'
        op1.setAttribute('value','rag doll')

        const op2 = document.getElementById('op2')
        op2.innerHTML = 'British Shorthairs'
        op2.setAttribute('value','british shorthairs')

        const op3 = document.getElementById('op3');
        op3.innerHTML = 'persian cat'
        op3.setAttribute('value','persian cat')

        const op4 = document.getElementById('op4');
        op4.innerHTML = 'Scottish Fold'
        op4.setAttribute('value','scotiish fold')
            
        }
        else if(dog=='parrot'){
            const op1 = document.getElementById('op1')
        op1.innerHTML = 'American Parrot'
        op1.setAttribute('value','american parrot')

        const op2 = document.getElementById('op2')
        op2.innerHTML = 'British Parrot'
        op2.setAttribute('value','british parrot')

        const op3 = document.getElementById('op3');
        op3.innerHTML = 'persian cat'
        op3.setAttribute('value','tota maina')

        const op4 = document.getElementById('op4');
        op4.innerHTML = 'indian'
        op4.setAttribute('value','indian')
            
        }

        else{
        const op1 = document.getElementById('op1')
        op1.innerHTML = 'American Fish'
        op1.setAttribute('value','american fish')

        const op2 = document.getElementById('op2')
        op2.innerHTML = 'Filter'
        op2.setAttribute('value','fighter')

        const op3 = document.getElementById('op3');
        op3.innerHTML = 'color full'
        op3.setAttribute('value','color full')

        const op4 = document.getElementById('op4');
        op4.innerHTML = 'indian'
        op4.setAttribute('value','indian')
            
        }
}
