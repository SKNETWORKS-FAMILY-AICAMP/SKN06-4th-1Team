function check_valid(name, birthday){
    var this_year = new Date().getFullYear();
    var age = this_year - birthday.substring(0,4);

    if(age < 8 || age > 100){
        return false;
    }

    if(name.length < 2){
        return false;
    }
}