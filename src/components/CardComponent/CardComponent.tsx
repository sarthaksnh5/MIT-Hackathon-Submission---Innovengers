import { View, ViewProps } from 'react-native'
import React, { ReactNode } from 'react'

interface CardComponentProps extends ViewProps {
    children: ReactNode
    className?: string
}

const CardComponent: React.FC<CardComponentProps> = ({ children, className = '', ...rest }) => {
    return (
        <View
            className={`w-5/6 p-4 flex items-center justify-center bg-white rounded-lg ${className}`}
            style={{ elevation: 1 }}
            {...rest}
        >
            {children}
        </View>
    )
}

export default CardComponent
