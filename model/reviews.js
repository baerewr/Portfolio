module.exports = function(sequelize, DataTypes){
    return sequelize.define('reviews',{
        idx: {
            type:DataTypes.INTEGER,
            autoIncrement:true,
            primaryKey:true,
            allwNull:false
        },
        movie_id: {
            type:DataTypes.STRING(250)
        },
        review:{
            type:DataTypes.TEXT
        }
    })
}